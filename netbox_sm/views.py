from netbox.views import generic
from utilities.views import register_model_view
from django.views.generic import FormView
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.urls import reverse 

from virtualization.models import VirtualMachine 
from virtualization.tables import VirtualMachineTable  
from dcim.models import Device
from dcim.tables import DeviceTable
from . import models, tables, forms
from . import base_views
from .models import Deployment, Component
from .tables import DeploymentTable
from .filtersets import DeploymentFilterSet, SolutionFilterSet, ComponentFilterSet

from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

def get_model_class(app_label, model_name):
    # Use ContentType to get the model class
    content_type = get_object_or_404(ContentType, app_label=app_label, model=model_name)
    return content_type.model_class()

class GenericAttachView(FormView):
    template_name = "netbox_sm/attach_form.html"
    form_class = forms.AttachForm

    def get_form_kwargs(self):
        # Get the default form kwargs
        kwargs = super().get_form_kwargs()

        # Dynamically determine the related model class from app_label and model_name
        related_model_class = get_model_class(self.kwargs['app_label'], self.kwargs['model_name'])
        
        # Get the current object to which we are attaching
        current_object = get_object_or_404(related_model_class, pk=self.kwargs['pk'])

        # Pass the current object and related model class to the form
        kwargs['current_object'] = current_object
        kwargs['related_model_class'] = related_model_class
        return kwargs

    def form_valid(self, form):
        # Attach the selected object to the current object
        existing_object = form.cleaned_data['existing_object']
        current_object = form.cleaned_data['current_object']

        # Here, use the correct relationship field to attach the object
        current_object.your_relationship_field.add(existing_object)

        # Redirect to a success page or the object detail page
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect to the object's detail view after successful attachment
        return reverse(
            f'plugins:{self.kwargs["app_label"]}:{self.kwargs["model_name"]}',  # Generate the correct detail view name
            kwargs={'pk': self.kwargs['pk']}
        )      
        
# SLO Views
class SLOListView(generic.ObjectListView):
    queryset = models.SLO.objects.all()
    table = tables.SLOTable

class SLODetailView(base_views.BaseObjectView):
    queryset = models.SLO.objects.all()

class SLOEditView(generic.ObjectEditView):
    queryset = models.SLO.objects.all()
    form = forms.SLOForm

class SLODeleteView(generic.ObjectDeleteView):
    queryset = models.SLO.objects.all()

class SLOBulkImportView(generic.BulkImportView):
    queryset = models.SLO.objects.all()
    model_form = forms.SLOImportForm

class SLOChangeLogView(base_views.BaseChangeLogView):
    base_model = models.SLO


# Solution Views
class SolutionListView(generic.ObjectListView):
    queryset = Solution.objects.all()
    filterset = SolutionFilterSet
    table = SolutionTable
    
class SolutionDetailView(base_views.BaseObjectView):
    queryset = models.Solution.objects.all()    
        
class SolutionEditView(generic.ObjectEditView):
    queryset = models.Solution.objects.all()
    form = forms.SolutionForm

class SolutionDeleteView(generic.ObjectDeleteView):
    queryset = models.Solution.objects.all()

class SolutionBulkImportView(generic.BulkImportView):
    queryset = models.Solution.objects.all()
    model_form = forms.SolutionImportForm

class SolutionChangeLogView(base_views.BaseChangeLogView):
    base_model = models.Solution


# FaultTolerence Views
class FaultTolerenceListView(generic.ObjectListView):
    queryset = models.FaultTolerence.objects.all()
    table = tables.FaultTolerenceTable

class FaultTolerenceDetailView(base_views.BaseObjectView):
    queryset = models.FaultTolerence.objects.all()

class FaultTolerenceEditView(generic.ObjectEditView):
    queryset = models.FaultTolerence.objects.all()
    form = forms.FaultTolerenceForm

class FaultTolerenceDeleteView(generic.ObjectDeleteView):
    queryset = models.FaultTolerence.objects.all()

class FaultTolerenceBulkImportView(generic.BulkImportView):
    queryset = models.FaultTolerence.objects.all()
    model_form = forms.FaultTolerenceImportForm

class FaultTolerenceChangeLogView(base_views.BaseChangeLogView):
    base_model = models.FaultTolerence

# Deployment Views
class DeploymentListView(generic.ObjectListView):
    queryset = models.Deployment.objects.all()
    table = tables.DeploymentTable
    filterset = DeploymentFilterSet
    
class DeploymentDetailView(generic.ObjectView):
    queryset = models.Deployment.objects.all()
    template_name = 'netbox_sm/deployment-detail.html'

    def get_extra_context(self, request, instance):
        deployment = instance
        solution = deployment.deployment_solution if deployment else None
        related_vms = VirtualMachine.objects.none()
        related_devices = Device.objects.none()
        other_deployments = Deployment.objects.none()
        grouped_fields = {}

        if deployment:
            # Get content types for Device and VirtualMachine
            vm_content_type = ContentType.objects.get_for_model(VirtualMachine)
            device_content_type = ContentType.objects.get_for_model(Device)

            # Query components associated with this deployment
            components = Component.objects.filter(component_deployment=deployment)
            component_vm_ids = components.filter(object_type=vm_content_type).values_list('object_id', flat=True)
            component_device_ids = components.filter(object_type=device_content_type).values_list('object_id', flat=True)

            # Query related VMs and Devices by component IDs
            related_vms = VirtualMachine.objects.filter(id__in=component_vm_ids)
            related_devices = Device.objects.filter(id__in=component_device_ids)

            if solution and hasattr(solution, 'project_id') and solution.project_id:
                project_id = solution.project_id + '-' + deployment.deployment_type.lower()
             
                # Query VMs and Devices by project_id prefix for completeness
                name_based_vms = VirtualMachine.objects.filter(name__startswith=project_id)
                name_based_devices = Device.objects.filter(name__startswith=project_id)

                # Combine component-based and name-based queries
                related_vms = VirtualMachine.objects.filter(
                    Q(id__in=component_vm_ids) | Q(name__startswith=project_id)
                ).distinct()
                related_devices = Device.objects.filter(
                    Q(id__in=component_device_ids) | Q(name__startswith=project_id)
                ).distinct()

                # Query other deployments for the same solution
                other_deployments = Deployment.objects.filter(deployment_solution=solution).exclude(pk=deployment.pk)

                # Define field groups for Solution
                field_groups = {
                    'Ownership and Contacts': [
                        'requester', 'architect', 'business_owner_group', 'business_owner_contact', 'incident_contact',
                        'os_technical_contact_group', 'os_technical_contact', 'app_technical_contact_group', 'app_technical_contact'
                    ],
                    'Compliance and Resilience': [
                        'data_classification', 'compliance_requirements', 'fault_tolerance', 'slos',
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

        # Instantiate tables and debug columns
        related_vms = VirtualMachineTable(related_vms)
        print("DeploymentDetailView VirtualMachineTable columns:", [col.name for col in related_vms.columns])  # Debug
        related_devices = DeviceTable(related_devices)
        print("DeploymentDetailView DeviceTable columns:", [col.name for col in related_devices.columns])  # Debug
        other_deployments = DeploymentTable(other_deployments)

        return {
            'solution': solution,
            'deployment': deployment,
            'related_vms': related_vms,
            'related_devices': related_devices,
            'other_deployments': other_deployments,
            'grouped_fields': grouped_fields,
        }
        
class DeploymentEditView(generic.ObjectEditView):
    queryset = models.Deployment.objects.all()
    form = forms.DeploymentForm

class DeploymentDeleteView(generic.ObjectDeleteView):
    queryset = models.Deployment.objects.all()

class DeploymentBulkImportView(generic.BulkImportView):
    queryset = models.Deployment.objects.all()
    model_form = forms.DeploymentImportForm

class DeploymentChangeLogView(base_views.BaseChangeLogView):
    base_model = models.Deployment

# Component Views
class ComponentListView(generic.ObjectListView):
    queryset = models.Component.objects.all()
    table = tables.ComponentTable
    filterset = ComponentFilterSet
      
class ComponentDetailView(base_views.BaseObjectView):
    queryset = models.Component.objects.all()

class ComponentEditView(generic.ObjectEditView):
    queryset = models.Component.objects.all()
    form = forms.ComponentForm

class ComponentDeleteView(generic.ObjectDeleteView):
    queryset = models.Component.objects.all()

class ComponentBulkImportView(generic.BulkImportView):
    queryset = models.Component.objects.all()
    model_form = forms.ComponentImportForm

class ComponentChangeLogView(base_views.BaseChangeLogView):
    base_model = models.Component

@register_model_view(Device, 'deployment', path='deployment')
class DeviceDeploymentView(base_views.BaseDeviceDeploymentView):
    template_name = 'netbox_sm/deployment-tab.html'
    queryset = Device.objects.all()

@register_model_view(VirtualMachine, 'deployment', path='deployment')
class VMDeploymentView(base_views.BaseVMDeploymentView):
    template_name = 'netbox_sm/deployment-tab.html'
    queryset = VirtualMachine.objects.all()

# @register_model_view(models.Solution, 'diagram', path='diagram')
# class SolutionDiagramView(base_views.BaseDiagramView):
#     queryset = models.Solution.objects.all()

# @register_model_view(models.Deployment, 'dia
#                      gram', path='diagram')
# class DeploymentDiagramView(base_views.BaseDiagramView):
#     queryset = models.Deployment.objects.all()

# @register_model_view(models.Component, 'diagram', path='diagram')
# class ComponentDiagramView(base_views.BaseDiagramView): 
#     queryset = models.Component.objects.all()

# @register_model_view(Region, 'diagram', path='diagram')
# class RegionDiagramView(base_views.BaseDiagramView): 
#     queryset = Region.objects.all()   
        
# @register_model_view(Device, 'diagram', path='diagram')
# class DeviceDiagramView(base_views.BaseDiagramView): 
#     queryset = Device.objects.all()

# @register_model_view(VirtualMachine, 'diagram', path='diagram')
# class VMDiagramView(base_views.BaseDiagramView):
#     queryset = VirtualMachine.objects.all()     
    
# @register_model_view(Cluster, 'diagram', path='diagram')
# class ClusterDiagramView(base_views.BaseDiagramView):
#     queryset = Cluster.objects.all() 
   
