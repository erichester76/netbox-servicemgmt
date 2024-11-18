from netbox.views import generic
from django.urls import reverse
from utilities.views import ViewTab
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from . import tables 
import re



def sanitize_name(name):
    """
    Cleans up the name by removing or replacing characters not allowed in Mermaid diagrams.
    Currently removes parentheses and other special characters.
    """
    # Remove parentheses and replace other characters if needed
    clean_name = re.sub(r'[^\w\s]', '', name)  # Remove all non-alphanumeric characters except spaces
    #clean_name = re.sub(r'\s+', '_', clean_name)  # Replace spaces with underscores
    return clean_name

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
        for rel in instance._meta.get_fields():
            if rel.is_relation and rel.auto_created and not rel.concrete:
                related_model = rel.related_model
                related_objects = getattr(instance, rel.get_accessor_name()).all()
         
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
        
def generate_mermaid_code(obj, visited=None, depth=0):
    """
    Recursively generates the Mermaid code for the given object and its relationships.
    Tracks visited objects to avoid infinite loops, particularly through reverse relationships.
    """
    if visited is None:
        visited = set()

    relationships_to_follow = {
        # Virtualization/Networking models
        'virtualmachine': [ 'host' ], 
        'device': [ 'cluster', 'virtual_chassis', 'rack' ],
        'rack': [ 'location' ],
        'location': [ 'site' ],
        'site': [],  
        'tenant': [],  
        'contact': [], 
        
        # Service Management (servicemgmt) models
        'solutionrequest': [ 'sot_sr' ],
        'solutiontemplate': [ 'service_templates'],
        'servicetemplate': [ 'solution_templates', 'service_requirements', 'service_deployments' ],
        'servicerequirement': [ 'service_template', 'sc_components' ],
        'servicedeployment': [ 'service_template', 'sc_deployments' ],
        'servicecomponent': [ 'service_requirement', 'service_deployment', 'content_object' ],    
    }



  


    mermaid_code = ""
    indent = "    " * depth  # Indentation for readability

    # Get object identifier and mark it as visited
    obj_id = f"{obj._meta.model_name}_{obj.pk}"
    if obj_id in visited:
        return mermaid_code  # Stop if already visited

    visited.add(obj_id)  # Mark visited

    # Add the object to the diagram
    obj_name = sanitize_name(str(obj))
    if depth == 0:
        mermaid_code += f"{indent}{obj_id}[{obj_name}]:::color_{obj._meta.model_name.lower()}\n"
        if hasattr(obj, 'get_absolute_url'):
            mermaid_code += f'{indent}click {obj_id} "{obj.get_absolute_url()}"\n'

    # Get allowed relationships for this object
    allowed_relationships = relationships_to_follow.get(obj._meta.model_name, [])

    # Traverse forward relationships
    for field in obj._meta.get_fields():
        if field.name not in allowed_relationships:
            continue

        # Handle ForeignKey and OneToOneField relationships
        if isinstance(field, (models.ForeignKey, models.OneToOneField)):
            related_obj = getattr(obj, field.name, None)
            if related_obj and related_obj.pk:
                related_obj_id = f"{related_obj._meta.model_name}_{related_obj.pk}"
                related_obj_name = sanitize_name(str(related_obj))
                if related_obj_id in visited:
                    continue  # Skip if already visited
                indent = "    " * (depth + 1)
                mermaid_code += f"{indent}{related_obj_id}({related_obj_name}):::color_{related_obj._meta.model_name.lower()}\n"
                mermaid_code += f"{indent}{obj_id} --> {related_obj_id}\n"
                mermaid_code += generate_mermaid_code(related_obj, visited, depth + 1)

    # Traverse reverse relationships (many-to-one, many-to-many)
    for rel in obj._meta.get_fields():
        if not rel.is_relation or not rel.auto_created or rel.concrete:
            continue

        related_objects = getattr(obj, rel.get_accessor_name(), None)
        if hasattr(related_objects, 'all') and rel.get_accessor_name() in allowed_relationships:
            for related_obj in related_objects.all():
                related_obj_id = f"{related_obj._meta.model_name}_{related_obj.pk}"
                related_obj_name = sanitize_name(str(related_obj))
                if related_obj_id in visited:
                    continue  # Skip if already visited
                indent = "    " * (depth + 1)
                mermaid_code += f"{indent}{related_obj_id}({related_obj_name}):::color_{related_obj._meta.model_name.lower()}\n"
                if hasattr(related_obj, 'get_absolute_url'):
                    mermaid_code += f'{indent}click {related_obj_id} "{related_obj.get_absolute_url()}"\n'
                mermaid_code += f"{indent}{obj_id} --> {related_obj_id}\n"
                mermaid_code += generate_mermaid_code(related_obj, visited, depth + 1)

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
        }
       for obj_type, color in color_map.items():
          mermaid_source += f'classDef color_{obj_type} fill:{color},stroke:#000,stroke-width:0px,color:#fff,font-size:14px;\n'

       return {
          'mermaid_source': mermaid_source,
       }


