from netbox.views import generic
from django.urls import reverse
from utilities.views import ViewTab
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from . import tables 
from .models import Solution,Deployment,Component
from django.db.models import Q
from virtualization.models import VirtualMachine 
from virtualization.tables import VirtualMachineTable  
from dcim.models import Device
from dcim.tables import DeviceTable
from .models import Solution, Deployment
from .tables import DeploymentTable
import re


DEPLOYMENT_TYPES = [
    ('p','Production'),
    ('g','Upgrade'),
    ('q','Quality Assurance'),
    ('u','User Acceptance Testing (UAT)'),
    ('d','Development'),
    ('s','Staging'),
    ('y','Prototype'),
    ('l','Learning/Training'),
    ('m','(Maintenance) Production Support'),
    ('n','Non-production'),
    ('f','Functional'),
    ('r','Disaster Recovery'),
    ('c','Secondary/Failover'),
    ('z','Sandbox'),
    ('o','Demo'),
]

color_map = {
            'solutiontemplate': '#16a2b8',  # Darker Teal
            'servicetemplate': '#184990',   # Teal
            'servicerequirement': '#f39c12',  # Yellow
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

def sanitize_name(name):
    """
    Cleans up the name by removing or replacing characters not allowed in Mermaid diagrams.
    Currently removes parentheses and other special characters.
    """
    # Remove parentheses and replace other characters if needed
    clean_name = re.sub(r'[^\w\s\-]', '', name)  # Remove all non-alphanumeric characters except spaces
    #clean_name = re.sub(r'\-', '_', clean_name)  # Replace spaces with underscores
    return clean_name

class BaseChangeLogView(generic.ObjectChangeLogView):
    base_template = 'netbox_sm/default-detail.html'
    
class BaseObjectView(generic.ObjectView):
    template_name = 'netbox_sm/default-detail.html'
    
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
                        f'plugins:netbox_sm:{model_name}_add'
                    )   
                    # Pre-fill the linking field with the current object's ID, if possible
                    add_url += f'?{instance._meta.model_name.lower()}={instance.pk}'
                    content_type = ContentType.objects.get_for_model(instance)
                    attach_url = reverse('plugins:netbox_sm:generic_attach', kwargs={
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

    # Relationships to follow for each model
    relationships_to_follow = {
        'solutionrequest': ['solreq_soltems'],
        'solutiontemplate': ['servtem_soltems'],
        'servicetemplate': ['servreq_servtems', 'servdep_servtems'],
        'servicerequirement': ['servcom_servreqs'],
        'servicedeployment': ['servcom_servdeps', 'servreq_servdeps'],
        'servicecomponent': [ 'content_object'],
        'virtualmachine': ['device', 'cluster' ],
        'vminterface': ['ip_addresses'],
        'device': ['virtual_chassis' ],
        'cluster': ['site'],
        'rack': ['location'],
        'location': ['site'],
        'site': [ ],
        'region': ['parent', 'site'],
        'certificate': ['hostnames'],
        'hostname': ['certificates'],
    }
    #     relationships_to_follow = {
    #     'virtualmachine': ['device', 'interfaces', 'virtualdisks'],
    #     'device': ['virtual_chassis', 'interfaces', 'cluster', 'rack'],
    #     'interface': ['ip_addresses'],
    #     'vminterface': ['ip_addresses'],
    #     'ipaddress': [ 'prefix'],
    #     'cluster': ['site'],
    #     'rack': ['location'],
    #     'location': ['site'],
    #     'site': [],
    #     'certificate': ['hostnames'],
    #     'hostname': ['certificates'],
    # }

    mermaid_code = ""
    indent = ""  

    if visited == None:
        visited=set()

    obj_id = f"{obj._meta.model_name}_{obj.pk}"
    obj_name = sanitize_name(str(obj))  # Sanitize the related object name
    
    if depth == 0: 
        mermaid_code += f"{indent}{obj_id}[{obj_name}]:::color_{obj._meta.model_name.lower()}\n"
        if hasattr(obj, 'get_absolute_url'):
            mermaid_code += f'{indent}click {obj_id} "{obj.get_absolute_url()}"\n'

    # Traverse forward relationships (ForeignKey, OneToOneField, GenericForeignKey)
    for field in obj._meta.get_fields():
        # Skip visited relationships
        if (obj_name,obj_id,field.name) in visited:
            continue
        # Skip excluded relationships
        if field.name not in relationships_to_follow.get(obj._meta.model_name, []):
            #print(f"skipping {obj} -> {field.name}")
            continue
        visited.add((obj_name,obj_id,field.name))
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
                    mermaid_code += f"{indent}{related_obj_id}({related_obj._meta.model_name}: {related_obj_name}):::color_{related_obj._meta.model_name.lower()}\n"
                    if hasattr(related_obj, 'get_absolute_url'):
                        mermaid_code += f'{indent}click {related_obj_id} "{related_obj.get_absolute_url()}"\n'
                    mermaid_code += f"{indent}{obj_id} --- {related_obj_id}\n"
                    mermaid_code += generate_mermaid_code(related_obj, visited, depth + 1)
                except related_model.DoesNotExist:
                    continue  # If the related object doesn't exist, skip it

        # Handle ForeignKey and OneToOneField relationships
        elif field.is_relation and not field.auto_created and field.concrete:
            # Check if the related object exists
            related_obj = getattr(obj, field.name, None)
            if related_obj and related_obj.pk:
                related_obj_id = f"{related_obj._meta.model_name}_{related_obj.pk}"
                related_obj_name = sanitize_name(str(related_obj))  # Sanitize the related object name
                mermaid_code += f"{indent}{related_obj_id}({field.name}: {related_obj_name}):::color_{related_obj._meta.model_name.lower()}\n"
                mermaid_code += f"{indent}{obj_id} --- {related_obj_id}\n"
                mermaid_code += generate_mermaid_code(related_obj, visited, depth + 1)
      
        elif field.is_relation and field.auto_created and not field.concrete:
            related_objects = getattr(obj, field.get_accessor_name(), None)
            if hasattr(related_objects, 'all'):
                for related_obj in related_objects.all():
                    related_obj_id = f"{related_obj._meta.model_name}_{related_obj.pk}"
                    related_obj_name = sanitize_name(str(related_obj))  # Sanitize the related object name
                    mermaid_code += f"{indent}{related_obj_id}({related_obj_name}):::color_{related_obj._meta.model_name.lower()}\n"
                    if hasattr(related_obj, 'get_absolute_url'):
                        mermaid_code += f'{indent}click {related_obj_id} "{related_obj.get_absolute_url()}"\n'
                    mermaid_code += f"{indent}{obj_id} --- {related_obj_id}\n"
                    mermaid_code += generate_mermaid_code(related_obj, visited, depth + 1)
    
    return mermaid_code

class BaseDiagramView(generic.ObjectView):    
    """
    Diagram tab View to show mermiad diagram of relationships of object
    """
    
    template_name = "netbox_sm/default-diagram.html"  
    
    tab = ViewTab(
        label='Diagram',
        badge=lambda obj: 1, 
    )
    
    def get_extra_context(self, request, instance):
        mermaid_source = "%%{ init: { 'flowchart': { 'curve': 'stepBefore' } } }%%\n"
        mermaid_source += "graph LR\n" 
        #recurse object relationships to build flowchart
        mermaid_source += generate_mermaid_code(instance)        
        link_styles = {}
        current_iteration = 0
        for line in mermaid_source.splitlines():
            if "--" in line: 
                parts = line.split("--")
                if len(parts) > 0:
                    source_obj = parts[0].strip()
                    obj_type = source_obj.split("_")[0] 
                    if obj_type not in link_styles:
                        link_styles[obj_type] = [] 
                    link_styles[obj_type].append(str(current_iteration))
                current_iteration += 1 
        for obj_type, color in color_map.items():
            mermaid_source += f'classDef color_{obj_type} fill:{color},stroke:#000,stroke-width:1px,color:#fff,font-size:16px;\n'
        for obj_type, link_indices in link_styles.items():
            indices = ",".join(link_indices)  
            mermaid_source += f"linkStyle {indices} stroke:{color_map[obj_type]},stroke-width:2px;\n"

        return {
          'mermaid_source': mermaid_source,
    }


class BaseVMSolutionView(generic.ObjectView):
    model = VirtualMachine
    tab = ViewTab(
        label='Solution',
        badge=lambda obj: Solution.objects.filter(project_id='-'.join(obj.name.split('-')[:2])).count() if obj.name else 0,
    )

    def get_extra_context(self, request, instance):
        vm = instance
        solution = None
        deployment = None
        related_vms = VirtualMachine.objects.none()
        related_devices = Device.objects.none()
        other_deployments = Deployment.objects.none()
        grouped_fields = {}

        if vm and hasattr(vm, 'name') and vm.name:
            vm_prefix = '-'.join(vm.name.split('-')[:2])
            vm_full_prefix = vm.name[:9]
            deployment_type_char = vm.name[8].lower() if len(vm.name) > 8 else None
            
            # Get content types for Device and VirtualMachine
            vm_content_type = ContentType.objects.get_for_model(VirtualMachine)
            device_content_type = ContentType.objects.get_for_model(Device)

            try:
                solution = Solution.objects.get(project_id=vm_prefix)
            except Solution.DoesNotExist:
                solution = None
            except Solution.MultipleObjectsReturned:
                solution = Solution.objects.filter(project_id=vm_prefix).first()

            if solution:
                if deployment_type_char:
                    deployment = Deployment.objects.filter(
                        deployment_solution=solution,
                        deployment_type=deployment_type_char
                    ).first()

                # Query related VMs and Devices by name prefix and components
                related_vms = VirtualMachine.objects.filter(name__startswith=vm_full_prefix)
                related_devices = Device.objects.filter(name__startswith=vm_full_prefix)

                if deployment:
                    components = Component.objects.filter(component_deployment=deployment)
                    component_vm_ids = components.filter(object_type=vm_content_type).values_list('object_id', flat=True)
                    component_device_ids = components.filter(object_type=device_content_type).values_list('object_id', flat=True)
                    
                    related_vms = VirtualMachine.objects.filter(
                        Q(id__in=component_vm_ids) | Q(name__startswith=vm_full_prefix)
                    ).distinct()
                    related_devices = Device.objects.filter(
                        Q(id__in=component_device_ids) | Q(name__startswith=vm_full_prefix)
                    ).distinct()

                other_deployments = Deployment.objects.filter(deployment_solution=solution).exclude(pk=deployment.pk if deployment else None)

                field_groups = {
                  'Solution Details': [
                        'name', 'solution_number', 'project_id', 'description', 'solution_type', 'version',
                        'status', 'previous_version'
                    ],
                    'Ownership and Contacts': [
                        'requester', 'architect', 'business_owner_group', 'business_owner_contact', 'incident_contact',
                        'os_technical_contact_group', 'os_technical_contact', 'app_technical_contact_group', 'app_technical_contact'
                    ],
                    'Compliance and Resilience': [
                        'data_classification', 'compliance_requirements', 'fault_tolerence', 'slos',
                        'last_bcdr_test', 'last_risk_assessment', 'last_review', 'production_readiness_status', 'vendor_management_status'
                    ],
                }

                for group_name, field_names in field_groups.items():
                    grouped_fields[group_name] = [
                        {
                            'name': field.name,
                            'verbose_name': field.verbose_name,
                            'value': getattr(solution, field.name),
                            'has_url': hasattr(getattr(solution, field.name), 'get_absolute_url') if getattr(solution, field.name) else False,
                        }
                        for field in solution._meta.fields
                        if field.name in field_names
                    ]

        # Configure tables with limited fields
        related_vms = VirtualMachineTable(related_vms)
        related_devices = DeviceTable(related_devices)
        other_deployments = DeploymentTable(other_deployments)

        return {
            'vm': vm,
            'solution': solution,
            'deployment': deployment,
            'related_vms': related_vms,
            'related_devices': related_devices,
            'other_deployments': other_deployments,
            'grouped_fields': grouped_fields,
        }

class BaseDeviceSolutionView(generic.ObjectView):
    model = Device
    tab = ViewTab(
        label='Solution',
        badge=lambda obj: Solution.objects.filter(project_id='-'.join(obj.name.split('-')[:2])).count() if obj.name else 0,
    )

    def get_extra_context(self, request, instance):
        device = instance
        solution = None
        deployment = None
        related_vms = VirtualMachine.objects.none()
        related_devices = Device.objects.none()
        other_deployments = Deployment.objects.none()
        grouped_fields = {}

        if device and hasattr(device, 'name') and device.name:
            device_prefix = '-'.join(device.name.split('-')[:2])
            device_full_prefix = device.name[:9]
            deployment_type_char = device.name[8].lower() if len(device.name) > 8 else None
            
            # Get content types for Device and VirtualMachine
            vm_content_type = ContentType.objects.get_for_model(VirtualMachine)
            device_content_type = ContentType.objects.get_for_model(Device)

            try:
                solution = Solution.objects.get(project_id=device_prefix)
            except Solution.DoesNotExist:
                solution = None
            except Solution.MultipleObjectsReturned:
                solution = Solution.objects.filter(project_id=device_prefix).first()

            if solution:
                if deployment_type_char:
                    deployment = Deployment.objects.filter(
                        deployment_solution=solution,
                        deployment_type=deployment_type_char
                    ).first()

                # Query related VMs and Devices by name prefix and components
                related_vms = VirtualMachine.objects.filter(name__startswith=device_full_prefix)
                related_devices = Device.objects.filter(name__startswith=device_full_prefix)

                if deployment:
                    components = Component.objects.filter(component_deployment=deployment)
                    component_vm_ids = components.filter(object_type=vm_content_type).values_list('object_id', flat=True)
                    component_device_ids = components.filter(object_type=device_content_type).values_list('object_id', flat=True)
                    
                    related_vms = VirtualMachine.objects.filter(
                        Q(id__in=component_vm_ids) | Q(name__startswith=device_full_prefix)
                    ).distinct()
                    related_devices = Device.objects.filter(
                        Q(id__in=component_device_ids) | Q(name__startswith=device_full_prefix)
                    ).distinct()

                other_deployments = Deployment.objects.filter(deployment_solution=solution).exclude(pk=deployment.pk if deployment else None)

                field_groups = {
                    'Solution Details': [
                        'name', 'solution_number', 'project_id', 'description', 'solution_type', 'version',
                        'status', 'previous_version'
                    ],
                    'Ownership and Contacts': [
                        'requester', 'architect', 'business_owner_group', 'business_owner_contact', 'incident_contact',
                        'os_technical_contact_group', 'os_technical_contact', 'app_technical_contact_group', 'app_technical_contact'
                    ],
                    'Compliance and Resilience': [
                        'data_classification', 'compliance_requirements', 'fault_tolerence', 'slos',
                        'last_bcdr_test', 'last_risk_assessment', 'last_review', 'production_readiness_status', 'vendor_management_status'
                    ],
                }

                for group_name, field_names in field_groups.items():
                    grouped_fields[group_name] = [
                        {
                            'name': field.name,
                            'verbose_name': field.verbose_name,
                            'value': getattr(solution, field.name),
                            'has_url': hasattr(getattr(solution, field.name), 'get_absolute_url') if getattr(solution, field.name) else False,
                        }
                        for field in solution._meta.fields
                        if field.name in field_names
                    ]

        # Configure tables with limited fields
        related_vms = VirtualMachineTable(related_vms)
        related_devices = DeviceTable(related_devices)
        other_deployments = DeploymentTable(other_deployments)

        return {
            'device': device,
            'solution': solution,
            'deployment': deployment,
            'related_vms': related_vms,
            'related_devices': related_devices,
            'other_deployments': other_deployments,
            'grouped_fields': grouped_fields,
        }