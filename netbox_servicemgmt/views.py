from netbox.views import generic
from . import base_views
from utilities.views import register_model_view, ViewTab
from django.views.generic import FormView
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.urls import reverse  # Import reverse

from . import models, tables, views, forms

from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import FormView


def get_model_class(app_label, model_name):
    # Use ContentType to get the model class
    content_type = get_object_or_404(ContentType, app_label=app_label, model=model_name)
    return content_type.model_class()

class GenericAttachView(FormView):
    template_name = "netbox_servicemgmt/attach_form.html"
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
        return reverse('plugins:netbox_servicemgmt:yourmodel_detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        # Attach the selected object to the current object
        existing_object = form.cleaned_data['existing_object']
        current_object = form.cleaned_data['current_object']

        # Example: Attach the existing object using a ManyToManyField (adjust as needed)
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



# Fault Tolerence Views
class SolutionRequestListView(generic.ObjectListView):
    queryset = models.SolutionRequest.objects.all()
    table = tables.SolutionRequestTable

class SolutionRequestDetailView(base_views.BaseObjectView):
    queryset = models.SolutionRequest.objects.all()

class SolutionRequestEditView(generic.ObjectEditView):
    queryset = models.SolutionRequest.objects.all()
    form = forms.SolutionRequestForm

class SolutionRequestDeleteView(generic.ObjectDeleteView):
    queryset = models.SolutionRequest.objects.all()

class SolutionRequestBulkImportView(generic.BulkImportView):
    queryset = models.SolutionRequest.objects.all()
    model_form = forms.SolutionRequestImportForm

class SolutionRequestChangeLogView(base_views.BaseChangeLogView):
    base_model = models.SolutionRequest


# Solution Template Views
class SolutionTemplateListView(generic.ObjectListView):
    queryset = models.SolutionTemplate.objects.all()
    table = tables.SolutionTemplateTable

@register_model_view(models.SolutionTemplate)
class SolutionTemplateDetailView(base_views.BaseObjectView):
    queryset = models.SolutionTemplate.objects.all()

@register_model_view(models.SolutionTemplate, 'diagram', path='diagram')
class SolutionTemplateDiagramView(base_views.BaseDiagramView):
    """
    Diagram tab for SolutionTemplate model.
    """
    queryset = models.SolutionTemplate.objects.all()

class SolutionTemplateEditView(generic.ObjectEditView):
    queryset = models.SolutionTemplate.objects.all()
    form = forms.SolutionTemplateForm

class SolutionTemplateDeleteView(generic.ObjectDeleteView):
    queryset = models.SolutionTemplate.objects.all()

class SolutionTemplateBulkImportView(generic.BulkImportView):
    queryset = models.SolutionTemplate.objects.all()
    model_form = forms.SolutionTemplateImportForm

class SolutionTemplateChangeLogView(base_views.BaseChangeLogView):
    base_model = models.SolutionTemplate


# Solution Request Views
class FaultToleranceListView(generic.ObjectListView):
    queryset = models.FaultTolerance.objects.all()
    table = tables.FaultToleranceTable

class FaultToleranceDetailView(base_views.BaseObjectView):
    queryset = models.FaultTolerance.objects.all()

class FaultToleranceEditView(generic.ObjectEditView):
    queryset = models.FaultTolerance.objects.all()
    form = forms.FaultToleranceForm

class FaultToleranceDeleteView(generic.ObjectDeleteView):
    queryset = models.FaultTolerance.objects.all()

class FaultToleranceBulkImportView(generic.BulkImportView):
    queryset = models.FaultTolerance.objects.all()
    model_form = forms.FaultToleranceImportForm

class FaultToleranceChangeLogView(base_views.BaseChangeLogView):
    base_model = models.FaultTolerance


# Service Template Views
class ServiceTemplateListView(generic.ObjectListView):
    queryset = models.ServiceTemplate.objects.all()
    table = tables.ServiceTemplateTable

@register_model_view(models.ServiceTemplate)
class ServiceTemplateDetailView(base_views.BaseObjectView):
    queryset = models.ServiceTemplate.objects.all()

@register_model_view(models.ServiceTemplate, 'diagram', path='diagram')
class ServiceTemplateDiagramView(base_views.BaseDiagramView):
    """
    Diagram tab for ServceTemplate model.
    """  
    queryset = models.ServiceTemplate.objects.all()

class ServiceTemplateEditView(generic.ObjectEditView):
    queryset = models.ServiceTemplate.objects.all()
    form = forms.ServiceTemplateForm

class ServiceTemplateDeleteView(generic.ObjectDeleteView):
    queryset = models.ServiceTemplate.objects.all()

class ServiceTemplateBulkImportView(generic.BulkImportView):
    queryset = models.ServiceTemplate.objects.all()
    model_form = forms.ServiceTemplateImportForm

class ServiceTemplateChangeLogView(base_views.BaseChangeLogView):
    base_model = models.ServiceTemplate


# Service Requirement Views
class ServiceRequirementListView(generic.ObjectListView):
    queryset = models.ServiceRequirement.objects.all()
    table = tables.ServiceRequirementTable

class ServiceRequirementDetailView(base_views.BaseObjectView):
    queryset = models.ServiceRequirement.objects.all()

class ServiceRequirementEditView(generic.ObjectEditView):
    queryset = models.ServiceRequirement.objects.all()
    form = forms.ServiceRequirementForm
    template_name = 'netbox_servicemgmt/servicerequirement-form.html'

class ServiceRequirementDeleteView(generic.ObjectDeleteView):
    queryset = models.ServiceRequirement.objects.all()

class ServiceRequirementBulkImportView(generic.BulkImportView):
    queryset = models.ServiceRequirement.objects.all()
    model_form = forms.ServiceRequirementImportForm

class ServiceRequirementChangeLogView(base_views.BaseChangeLogView):
    base_model = models.ServiceRequirement


# Service Deployment Views
class ServiceDeploymentListView(generic.ObjectListView):
    queryset = models.ServiceDeployment.objects.all()
    table = tables.ServiceDeploymentTable

@register_model_view(models.ServiceDeployment)
class ServiceDeploymentDetailView(base_views.BaseObjectView):
    queryset = models.ServiceDeployment.objects.all()

@register_model_view(models.ServiceDeployment, 'diagram', path='diagram')
class ServiceDeploymentDiagramView(base_views.BaseDiagramView):
    """
    Diagram tab for ServiceDeployment model.
    """  
    queryset = models.ServiceDeployment.objects.all()

class ServiceDeploymentEditView(generic.ObjectEditView):
    queryset = models.ServiceDeployment.objects.all()
    form = forms.ServiceDeploymentForm

class ServiceDeploymentDeleteView(generic.ObjectDeleteView):
    queryset = models.ServiceDeployment.objects.all()

class ServiceDeploymentBulkImportView(generic.BulkImportView):
    queryset = models.ServiceDeployment.objects.all()
    model_form = forms.ServiceDeploymentImportForm

class ServiceDeploymentChangeLogView(base_views.BaseChangeLogView):
    base_model = models.ServiceDeployment


# Service Component Views
class ServiceComponentListView(generic.ObjectListView):
    queryset = models.ServiceComponent.objects.all()
    table = tables.ServiceComponentTable

class ServiceComponentDetailView(base_views.BaseObjectView):
    queryset = models.ServiceComponent.objects.all()

class ServiceComponentEditView(generic.ObjectEditView):
    queryset = models.ServiceComponent.objects.all()
    form = forms.ServiceComponentForm

class ServiceComponentDeleteView(generic.ObjectDeleteView):
    queryset = models.ServiceComponent.objects.all()

class ServiceComponentBulkImportView(generic.BulkImportView):
    queryset = models.ServiceComponent.objects.all()
    model_form = forms.ServiceComponentImportForm

class ServiceComponentChangeLogView(base_views.BaseChangeLogView):
    base_model = models.ServiceComponent
