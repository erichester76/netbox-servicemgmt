import re
from netbox.views import generic
from django.db.models.fields.related import ForeignKey, ManyToManyField, OneToOneField
from django.urls import reverse

from . import (
    filtersets, 
    forms, 
    tables,
    models
    )

class BaseChangeLogView(generic.ObjectChangeLogView):
    template_name = 'netbox_servicemgmt/default-detail.html'
    
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
            # Skip excluded fields
            if field.name in excluded_extras or field.related_model:
                continue      
            value = None
            url = None
            
            try:
                # Handle ForeignKey and OneToOne relationships
                if isinstance(field, (ForeignKey, OneToOneField)):
                    related_object = getattr(instance, field.name)
                    value = str(related_object) if related_object else None
                    if hasattr(related_object, 'get_absolute_url'):
                        url = related_object.get_absolute_url()
                # Handle regular fields
                else:
                    value = getattr(instance, field.name)
            except AttributeError:
                value = None  # In case the relationship doesn't exist or is optional

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
                if related_objects.exists():
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
                        related_table = table_class(related_objects)
                    else:
                        related_table = None

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
