from netbox.views import generic
from django.urls import reverse
from utilities.views import ViewTab
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from . import tables 
import re
import logging

logger = logging.getLogger('netbox.plugins.netbox_servicemgmt')

class BaseChangeLogView(generic.ObjectChangeLogView):
    base_template = 'netbox_servicemgmt/default-detail.html'
    
class BaseObjectView(generic.ObjectView):
    template_name = 'netbox_servicemgmt/default-detail.html'
    
    def get_extra_context(self, request, instance):
        # Extract fields and their values for the object, including relationships
        field_data = []
        object_name = instance._meta.verbose_name
        # Define fields to exclude
        excluded_extras = {
            'id', 
            'custom_field_data', 
            'tags', 
            'bookmarks', 
            'journal_entries', 
            'subscriptions', 
            'tagged_items', 
            'created',
            'last_updated',
            'object_id',
            'object_type'
        }

        # Extract fields and their values for the object, including relationships
        field_data = []
        for field in instance._meta.get_fields():      
            # Skip excluded fields listed above
            if field.name in excluded_extras or ('equirement' in field.name):
                continue      
            
            value = None
            url = None
            
            try:
                
                # display only forward relations, not reverse. reverse should be tables below
                if field.is_relation and not field.auto_created:
                    related_object = getattr(instance, field.name)
                    value = str(related_object)  
                    if hasattr(related_object, 'get_absolute_url'):
                        url = related_object.get_absolute_url()
                #handle normal fields
                elif not field.is_relation:
                    value = getattr(instance, field.name)
                else:
                    continue
                    
            except AttributeError:
                value = None  

            field_data.append({
                'name': field.verbose_name if hasattr(field, 'verbose_name') else field.name,
                'value': value,
                'url': url, 
            })

        # Find reverse relations dynamically and add them to related_tables
        related_tables = []
        for field in instance._meta.get_fields():
            if field.is_relation and field.auto_created and not field.concrete:
                related_model = field.related_model
                related_objects = getattr(instance, field.get_accessor_name()).all()
         
                # Create the URL for adding a new related object
                add_url = None
                if hasattr(related_model, 'get_absolute_url'):
                    model_name = related_model._meta.model_name.lower()
                    add_url = reverse(
                        f'plugins:netbox_servicemgmt:{model_name}_add'
                    )   
                    # Pre-fill the linking field with the current object's ID, if possible
                    add_url += f'?{instance._meta.model_name.lower()}={instance.pk}'
                    content_type = ContentType.objects.get_for_model(instance)
                    attach_url = reverse('plugins:netbox_servicemgmt:generic_attach', kwargs={
                        'app_label': content_type.app_label,
                        'model_name': content_type.model,
                        'pk': instance.pk
                    })

                # Create a table dynamically if a suitable one exists
                table_class_name = f"{related_model.__name__}Table"
                if hasattr(tables, table_class_name):
                    table_class = getattr(tables, table_class_name)
                    # Always create the table, even if related_objects is empty
                    related_table = table_class(related_objects)
                else:
                    related_table = None

                # Append the table to related_tables even if there are no related objects
                related_tables.append({
                    'name': related_model._meta.verbose_name_plural,
                    'objects': related_objects,
                    'table': related_table,
                    'add_url': add_url,
                    'attach_url': attach_url,
                })

                    
        return {
            'object_name': object_name,
            'field_data': field_data,
            'related_tables': related_tables,
        }
    

def sanitize_name(name):
    """
    Cleans up the name by removing or replacing characters not allowed in Mermaid diagrams.
    Currently removes parentheses and other special characters.
    """
    # Remove parentheses and replace other characters if needed
    clean_name = re.sub(r'[^\w\s-]', '', name)  # Remove all non-alphanumeric characters except spaces
    clean_name = re.sub(r'-', '_', clean_name)  # Replace spaces with underscores
    return clean_name


def generate_mermaid_code(obj, visited=None, depth=0):
    """
    Generates the Mermaid code for the given object and its relationships.
    Traverses forward and reverse relationships based on a predefined filter.
    Handles `GenericForeignKey` relationships robustly.
    """
    if visited is None:
        visited = set()

    relationships_to_follow = {
        # Add relationships for each model
        'solutiontemplate': ['service_templates'],
        'servicetemplate': ['service_requirements', 'service_deployments'],
        'servicerequirement': ['sc_components'],
        'servicedeployment': ['sc_deployments'],
        'servicecomponent': ['content_object'],
        'virtualmachine': ['device'],
        'device': ['rack', 'cluster', 'virtual_chassis'],
        'rack': ['location'],
        'location': ['site'],
        'site': [],
        'tenant': [],
    }

    mermaid_code = ""
    obj_id = f"{obj._meta.model_name}_{obj.pk}"
    obj_name = str(obj)

    # Add root node
    if depth == 0:
        mermaid_code += f"{obj_id}[{obj_name}]:::color_{obj._meta.model_name.lower()}\n"
        if hasattr(obj, 'get_absolute_url'):
            mermaid_code += f'click {obj_id} "{obj.get_absolute_url()}"\n'

    # Traverse forward relationships
    for field in obj._meta.get_fields():
        try:
            if field.name in relationships_to_follow.get(obj._meta.model_name, []):
                related_obj = None

                # Handle `GenericForeignKey`
                if isinstance(field, GenericForeignKey):
                    content_type = getattr(obj, field.ct_field, None)
                    object_id = getattr(obj, field.fk_field, None)
                    if content_type and object_id:
                        try:
                            related_model = content_type.model_class()
                            related_obj = related_model.objects.get(pk=object_id)
                            print(f"GenericForeignKey points to: {related_obj}")
                        except related_model.DoesNotExist:
                            print(f"GenericForeignKey points to non-existent object: {content_type} with ID {object_id}")
                            continue

                # Handle regular forward relationships
                elif isinstance(field, (models.ForeignKey, models.OneToOneField)):
                    related_obj = getattr(obj, field.name, None)

                if related_obj and hasattr(related_obj, 'pk'):
                    related_obj_id = f"{related_obj._meta.model_name}_{related_obj.pk}"
                    if (related_obj_id, field.name) in visited:
                        continue

                    # Add to Mermaid code
                    visited.add((related_obj_id, field.name))
                    related_obj_name = str(related_obj)
                    mermaid_code += f"{related_obj_id}[{related_obj_name}]:::color_{related_obj._meta.model_name.lower()}\n"
                    if hasattr(related_obj, 'get_absolute_url'):
                        mermaid_code += f'click {related_obj_id} "{related_obj.get_absolute_url()}"\n'
                    mermaid_code += f"{related_obj_id} --> {obj_id}\n"
                    # Recurse
                    mermaid_code += generate_mermaid_code(related_obj, visited, depth + 1)

        except AttributeError as e:
            print(f"Error processing forward relationship {field.name}: {e}")
            continue

    # Traverse reverse relationships
    for rel in obj._meta.get_fields():
        if rel.is_relation and rel.auto_created and not rel.concrete:
            relationship_name = rel.get_accessor_name()
            try:
                related_objects_manager = getattr(obj, relationship_name, None)
                if related_objects_manager and hasattr(related_objects_manager, 'all'):
                    for related_obj in related_objects_manager.all():
                        related_obj_id = f"{related_obj._meta.model_name}_{related_obj.pk}"
                        if (related_obj_id, relationship_name) in visited:
                            continue
                        visited.add((related_obj_id, relationship_name))
                        related_obj_name = str(related_obj)
                        mermaid_code += f"{related_obj_id}[{related_obj_name}]:::color_{related_obj._meta.model_name.lower()}\n"
                        if hasattr(related_obj, 'get_absolute_url'):
                            mermaid_code += f'click {related_obj_id} "{related_obj.get_absolute_url()}"\n'
                        mermaid_code += f"{obj_id} --> {related_obj_id}\n"
                        # Recurse
                        mermaid_code += generate_mermaid_code(related_obj, visited, depth + 1)
            except AttributeError as e:
                print(f"Error processing reverse relationship {relationship_name}: {e}")
                continue
            except TypeError as e:
                print(f"TypeError processing reverse relationship {relationship_name}: {e}")
                continue

    return mermaid_code

class BaseDiagramView(generic.ObjectView):    
    """
    Diagram tab View to show mermiad diagram of relationships of object
    """
    
    template_name = "netbox_servicemgmt/default-diagram.html"  
    
    tab = ViewTab(
        label='Diagram',
        badge=lambda obj: 1, 
    )
    
    def get_extra_context(self, request, instance):
        mermaid_source = f"graph LR\n{generate_mermaid_code(instance)}"
        color_map = {
            'solutiontemplate': '#16a2b8',  # Darker Teal
            'servicetemplate': '#184990',   # Teal
            'servicerequirement': '#02252f',  # GreenBlue
            'servicedeployment': '#f76706',  # Orange2
            'servicecomponent': '#d63a39',  # Red
            'virtualmachine': '#9b59b6',  # Purple
            'device': '#2ecc71',  # Green
            'cluster': '#3498db',  # Light Blue
            'virtualchassis': '#34495e', # Gray-Blue
            'rack': '#9b59b6',  # Purple 
            'location': '#f39c12',  # Yellow
            'site': '#e74c3c',  # Red-Orange
            'tenant': '#1abc9c',  # Turquoise
            'contact': '#e67e22',  # Orange
            'certificate': '#8e44ad',  # Dark Purple
            'hostname': '#2980b9',  # Sky Blue
        }
        for obj_type, color in color_map.items():
          mermaid_source += f'classDef color_{obj_type} fill:{color},stroke:#000,stroke-width:0px,color:#fff,font-size:14px;\n'

        return {
          'mermaid_source': mermaid_source,
    }


