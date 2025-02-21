from netbox.views import generic
from . import base_views
from utilities.views import register_model_view
from django.views.generic import FormView
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.urls import reverse 
from dcim.models import Device, Region
from virtualization.models import VirtualMachine, Cluster
from . import models, tables, forms
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import FormView

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
    queryset = models.Solution.objects.all()
    table = tables.SolutionTable

#@register_model_view(models.Solution)
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

#@register_model_view(models.Deployment)
class DeploymentDetailView(base_views.BaseObjectView):
    queryset = models.Deployment.objects.all()

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

#@register_model_view(models.Component)
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

@register_model_view(VirtualMachine, 'solution', path='solution')
class VMSolutionView(base_views.BaseSolutionView):
    template_name = 'netbox_sm/vm_solution_tab.html'
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
   
