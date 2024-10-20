from netbox.views import generic
from .base_views import BaseObjectView, BaseChangeLogView, BaseDiagramView
from .models import SLO, SolutionTemplate, FaultTolerance, ServiceTemplate, ServiceRequirement, SolutionDeployment, ServiceDeployment, ServiceComponent
from .forms import AttachForm, SLOForm, SLOImportForm, SolutionTemplateForm, SolutionTemplateImportForm, FaultToleranceForm, FaultToleranceImportForm, ServiceTemplateForm, ServiceTemplateImportForm, ServiceRequirementForm, ServiceRequirementImportForm ,SolutionDeploymentForm, SolutionDeploymentImportForm, ServiceDeploymentForm, ServiceDeploymentImportForm, ServiceComponentForm, ServiceComponentImportForm
from .tables import SLOTable, SolutionTemplateTable, FaultToleranceTable, ServiceTemplateTable, ServiceRequirementTable, SolutionDeploymentTable, ServiceDeploymentTable, ServiceComponentTable
from utilities.views import register_model_view, ViewTab
from django.views.generic import FormView
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.urls import reverse  # Import reverse


from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import FormView
from .forms import AttachForm


def get_model_class(app_label, model_name):
    # Use ContentType to get the model class
    content_type = get_object_or_404(ContentType, app_label=app_label, model=model_name)
    return content_type.model_class()

class GenericAttachView(FormView):
    template_name = "netbox_servicemgmt/attach_form.html"
    form_class = AttachForm

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
    queryset = SLO.objects.all()
    table = SLOTable

class SLODetailView(BaseObjectView):
    queryset = SLO.objects.all()

class SLOEditView(generic.ObjectEditView):
    queryset = SLO.objects.all()
    form = SLOForm

class SLODeleteView(generic.ObjectDeleteView):
    queryset = SLO.objects.all()

class SLOBulkImportView(generic.BulkImportView):
    queryset = SLO.objects.all()
    model_form = SLOImportForm

class SLOChangeLogView(BaseChangeLogView):
    base_model = SLO


# Solution Template Views
class SolutionTemplateListView(generic.ObjectListView):
    queryset = SolutionTemplate.objects.all()
    table = SolutionTemplateTable

@register_model_view(SolutionTemplate)
class SolutionTemplateDetailView(BaseObjectView):
    queryset = SolutionTemplate.objects.all()

@register_model_view(SolutionTemplate, 'diagram', path='diagram')
class SolutionTemplateDiagramView(BaseDiagramView):
    """
    Diagram tab for SolutionTemplate model.
    """
    queryset = SolutionTemplate.objects.all()

class SolutionTemplateEditView(generic.ObjectEditView):
    queryset = SolutionTemplate.objects.all()
    form = SolutionTemplateForm

class SolutionTemplateDeleteView(generic.ObjectDeleteView):
    queryset = SolutionTemplate.objects.all()

class SolutionTemplateBulkImportView(generic.BulkImportView):
    queryset = SolutionTemplate.objects.all()
    model_form = SolutionTemplateImportForm

class SolutionTemplateChangeLogView(BaseChangeLogView):
    base_model = SolutionTemplate


# Fault Tolerence Views
class FaultToleranceListView(generic.ObjectListView):
    queryset = FaultTolerance.objects.all()
    table = FaultToleranceTable

class FaultToleranceDetailView(BaseObjectView):
    queryset = FaultTolerance.objects.all()

class FaultToleranceEditView(generic.ObjectEditView):
    queryset = FaultTolerance.objects.all()
    form = FaultToleranceForm

class FaultToleranceDeleteView(generic.ObjectDeleteView):
    queryset = FaultTolerance.objects.all()

class FaultToleranceBulkImportView(generic.BulkImportView):
    queryset = FaultTolerance.objects.all()
    model_form = FaultToleranceImportForm

class FaultToleranceChangeLogView(BaseChangeLogView):
    base_model = FaultTolerance


# Service Template Views
class ServiceTemplateListView(generic.ObjectListView):
    queryset = ServiceTemplate.objects.all()
    table = ServiceTemplateTable

@register_model_view(ServiceTemplate)
class ServiceTemplateDetailView(BaseObjectView):
    queryset = ServiceTemplate.objects.all()

@register_model_view(ServiceTemplate, 'diagram', path='diagram')
class ServiceTemplateDiagramView(BaseDiagramView):
    """
    Diagram tab for ServceTemplate model.
    """  
    queryset = ServiceTemplate.objects.all()

class ServiceTemplateEditView(generic.ObjectEditView):
    queryset = ServiceTemplate.objects.all()
    form = ServiceTemplateForm

class ServiceTemplateDeleteView(generic.ObjectDeleteView):
    queryset = ServiceTemplate.objects.all()

class ServiceTemplateBulkImportView(generic.BulkImportView):
    queryset = ServiceTemplate.objects.all()
    model_form = ServiceTemplateImportForm

class ServiceTemplateChangeLogView(BaseChangeLogView):
    base_model = ServiceTemplate


# Service Requirement Views
class ServiceRequirementListView(generic.ObjectListView):
    queryset = ServiceRequirement.objects.all()
    table = ServiceRequirementTable

class ServiceRequirementDetailView(BaseObjectView):
    queryset = ServiceRequirement.objects.all()

class ServiceRequirementEditView(generic.ObjectEditView):
    queryset = ServiceRequirement.objects.all()
    form = ServiceRequirementForm
    template_name = 'netbox_servicemgmt/servicerequirement-form.html'

class ServiceRequirementDeleteView(generic.ObjectDeleteView):
    queryset = ServiceRequirement.objects.all()

class ServiceRequirementBulkImportView(generic.BulkImportView):
    queryset = ServiceRequirement.objects.all()
    model_form = ServiceRequirementImportForm

class ServiceRequirementChangeLogView(BaseChangeLogView):
    base_model = ServiceRequirement


# Solution Deployment Views
class SolutionDeploymentListView(generic.ObjectListView):
    queryset = SolutionDeployment.objects.all()
    table = SolutionDeploymentTable

@register_model_view(SolutionDeployment)
class SolutionDeploymentDetailView(BaseObjectView):
    queryset = SolutionDeployment.objects.all()

@register_model_view(SolutionDeployment, 'diagram', path='diagram')
class SolutionDeploymentDiagramView(BaseDiagramView):
    """
    Diagram tab for SolutionDeployment model.
    """  
    queryset = SolutionDeployment.objects.all()


class SolutionDeploymentEditView(generic.ObjectEditView):
    queryset = SolutionDeployment.objects.all()
    form = SolutionDeploymentForm

class SolutionDeploymentDeleteView(generic.ObjectDeleteView):
    queryset = SolutionDeployment.objects.all()

class SolutionDeploymentBulkImportView(generic.BulkImportView):
    queryset = SolutionDeployment.objects.all()
    model_form = SolutionDeploymentImportForm

class SolutionDeploymentChangeLogView(BaseChangeLogView):
    base_model = SolutionDeployment


# Service Deployment Views
class ServiceDeploymentListView(generic.ObjectListView):
    queryset = ServiceDeployment.objects.all()
    table = ServiceDeploymentTable

@register_model_view(ServiceDeployment)
class ServiceDeploymentDetailView(BaseObjectView):
    queryset = ServiceDeployment.objects.all()

@register_model_view(ServiceDeployment, 'diagram', path='diagram')
class ServiceDeploymentDiagramView(BaseDiagramView):
    """
    Diagram tab for ServiceDeployment model.
    """  
    queryset = ServiceDeployment.objects.all()

class ServiceDeploymentEditView(generic.ObjectEditView):
    queryset = ServiceDeployment.objects.all()
    form = ServiceDeploymentForm

class ServiceDeploymentDeleteView(generic.ObjectDeleteView):
    queryset = ServiceDeployment.objects.all()

class ServiceDeploymentBulkImportView(generic.BulkImportView):
    queryset = ServiceDeployment.objects.all()
    model_form = ServiceDeploymentImportForm

class ServiceDeploymentChangeLogView(BaseChangeLogView):
    base_model = ServiceDeployment


# Service Component Views
class ServiceComponentListView(generic.ObjectListView):
    queryset = ServiceComponent.objects.all()
    table = ServiceComponentTable

class ServiceComponentDetailView(BaseObjectView):
    queryset = ServiceComponent.objects.all()

class ServiceComponentEditView(generic.ObjectEditView):
    queryset = ServiceComponent.objects.all()
    form = ServiceComponentForm

class ServiceComponentDeleteView(generic.ObjectDeleteView):
    queryset = ServiceComponent.objects.all()

class ServiceComponentBulkImportView(generic.BulkImportView):
    queryset = ServiceComponent.objects.all()
    model_form = ServiceComponentImportForm

class ServiceComponentChangeLogView(BaseChangeLogView):
    base_model = ServiceComponent
