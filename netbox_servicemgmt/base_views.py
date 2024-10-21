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
            if field.name in excluded_extras or ('Requirement' in field.name):
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

    excluded_fields = {
        'id', 
        'custom_field_data',
        'custom_fields', 
        'tags',
        'bookmarks', 
        'journal_entries', 
        'subscriptions', 
        'tagged_items', 
        'device_type',
        'device',
        'role',
        'ipaddress',
        'depends_on',
        'dependencies',
        'created',
        'last_updated',
        'object_id',
        'primary_ip4',
        'primary_ip6',
        'ipaddresses',
        'cluster_group',
        'cluster_type',
        'fault_tolerence',
        'service_slo',
        'vendor',
        'business_owner_contact',
        'business_owner_tenant',
        'service_owner_contact',
        'service_owner_tenant',
        'design_contact',
        'requirement_owner',
    }

    models_to_skip_reverse_relations = {
        'Site', 
        'Tenant',
        'Contact',
        'Site',
        'FaultTolerence',
        'SLO',
        'IPAddress',
        'Interface',
        'Manufacturer', 
        'Tag',       
    }

    mermaid_code = ""
    indent = "    " * depth  # Indentation for readability

    # Get object identifier and mark the object as visited to avoid revisiting it
    obj_id = f"{obj._meta.model_name}_{obj.pk}"
    if obj_id in visited:
        return mermaid_code  # Stop if this object was already visited

    visited.add(obj_id)  # Mark the object as visited *before* recursion

    # Add the object to the diagram
    obj_name = sanitize_name(str(obj))  # Sanitize the related object name
    mermaid_code += f"{indent}{obj_id}[{obj_name}]\n"

    # Traverse forward relationships (ForeignKey, OneToOneField, GenericForeignKey)
    for field in obj._meta.get_fields():
        # Skip excluded fields like 'tags'
        if field.name in excluded_fields:
            continue

        """# Handle ForeignKey and OneToOneField relationships
        if isinstance(field, (models.ForeignKey, models.OneToOneField)):
            # Check if the related object exists
            related_obj = getattr(obj, field.name, None)
            if related_obj and related_obj.pk:
                related_obj_id = f"{related_obj._meta.model_name}_{related_obj.pk}"
                related_obj_name = sanitize_name(str(related_obj))  # Sanitize the related object name
                if related_obj_id in visited:
                     continue  # Skip if already visited
                # Add relationship and recurse with indent for readability
                mermaid_code += f"{indent}{obj_id} --> {related_obj_id}[{related_obj_name}]\n"
                mermaid_code += generate_mermaid_code(related_obj, visited, depth + 1) 
        """

        # Handle GenericForeignKey
        if isinstance(field, GenericForeignKey):
            content_type = getattr(obj, field.ct_field, None)
            object_id = getattr(obj, field.fk_field, None)
            if content_type and object_id:
                related_model = content_type.model_class()
                try:
                    related_obj = related_model.objects.get(pk=object_id)
                    related_obj_id = f"{related_obj._meta.model_name}_{related_obj.pk}"
                    related_obj_name = sanitize_name(str(related_obj))  # Sanitize the related object name
                    if related_obj_id in visited:
                        continue  # Skip if already visited
                    # Add relationship and recurse with indent for readability
                    mermaid_code += f"{indent}{related_obj_id}[{related_obj_name}] --> {obj_id}\n"
                    mermaid_code += generate_mermaid_code(related_obj, visited, depth + 1)
                except related_model.DoesNotExist:
                    continue  # If the related object doesn't exist, skip it

    # Traverse reverse relationships (many-to-one, many-to-many)
    if obj._meta.model_name not in models_to_skip_reverse_relations:
        for rel in obj._meta.get_fields():
            if rel.is_relation and rel.auto_created and not rel.concrete:
                related_objects = getattr(obj, rel.get_accessor_name(), None)
                if hasattr(related_objects, 'all'):
                    for related_obj in related_objects.all():
                        related_obj_id = f"{related_obj._meta.model_name}_{related_obj.pk}"
                        related_obj_name = sanitize_name(str(related_obj))  # Sanitize the related object name
                        # Check if the related object was already visited to avoid loops
                        if related_obj_id in visited:
                            continue  # Skip if already visited
                        # Add reverse relationship and recurse with indent for readability
                        mermaid_code += f"{indent}{related_obj_id}[{related_obj_name}] --> {obj_id}\n"
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

       return {
          'mermaid_source': mermaid_source,
       }


