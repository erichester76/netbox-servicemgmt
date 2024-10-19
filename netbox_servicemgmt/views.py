from netbox.views import generic
from .base_view import BaseObjectView
from .models import SLO, SolutionTemplate, FaultTolerence, ServiceTemplate, ServiceRequirement, SolutionDeployment, ServiceDeployment, ServiceComponent
from .forms import SLOForm, SolutionTemplateForm, FaultTolerenceForm, ServiceTemplateForm, ServiceRequirementForm, SolutionDeploymentForm, ServiceDeploymentForm, ServiceComponentForm
from .tables import SLOTable, SolutionTemplateTable, FaultTolerenceTable, ServiceTemplateTable, ServiceRequirementTable, SolutionDeploymentTable, ServiceDeploymentTable, ServiceComponentTable

# SLO Views
class SLOListView(generic.ObjectListView):
    queryset = SLO.objects.all()
    table = SLOTable

class SLODetailView(generic.BaseObjectView):
    queryset = SLO.objects.all()

class SLOEditView(generic.ObjectEditView):
    queryset = SLO.objects.all()
    form = SLOForm

class SLODeleteView(generic.ObjectDeleteView):
    queryset = SLO.objects.all()

class SLOBulkImportView(generic.BulkImportView):
    queryset = SLO.objects.all()
    model_form = SLOForm

class SLOChangeLogView(generic.ObjectChangeLogView):
    base_model = SLO

# Solution Template Views
class SolutionTemplateListView(generic.ObjectListView):
    queryset = SolutionTemplate.objects.all()
    table = SolutionTemplateTable

class SolutionTemplateDetailView(generic.BaseObjectView):
    queryset = SolutionTemplate.objects.all()

class SolutionTemplateEditView(generic.ObjectEditView):
    queryset = SolutionTemplate.objects.all()
    form = SolutionTemplateForm

class SolutionTemplateDeleteView(generic.ObjectDeleteView):
    queryset = SolutionTemplate.objects.all()

class SolutionTemplateBulkImportView(generic.BulkImportView):
    queryset = SolutionTemplate.objects.all()
    model_form = SolutionTemplateForm

class SolutionTemplateChangeLogView(generic.ObjectChangeLogView):
    base_model = SolutionTemplate

# Fault Tolerence Views
class FaultTolerenceListView(generic.ObjectListView):
    queryset = FaultTolerence.objects.all()
    table = FaultTolerenceTable

class FaultTolerenceDetailView(generic.BaseObjectView):
    queryset = FaultTolerence.objects.all()

class FaultTolerenceEditView(generic.ObjectEditView):
    queryset = FaultTolerence.objects.all()
    form = FaultTolerenceForm

class FaultTolerenceDeleteView(generic.ObjectDeleteView):
    queryset = FaultTolerence.objects.all()

class FaultTolerenceBulkImportView(generic.BulkImportView):
    queryset = FaultTolerence.objects.all()
    model_form = FaultTolerenceForm

class FaultTolerenceChangeLogView(generic.ObjectChangeLogView):
    base_model = FaultTolerence

# Service Template Views
class ServiceTemplateListView(generic.ObjectListView):
    queryset = ServiceTemplate.objects.all()
    table = ServiceTemplateTable

class ServiceTemplateDetailView(generic.BaseObjectView):
    queryset = ServiceTemplate.objects.all()

class ServiceTemplateEditView(generic.ObjectEditView):
    queryset = ServiceTemplate.objects.all()
    form = ServiceTemplateForm

class ServiceTemplateDeleteView(generic.ObjectDeleteView):
    queryset = ServiceTemplate.objects.all()

class ServiceTemplateBulkImportView(generic.BulkImportView):
    queryset = ServiceTemplate.objects.all()
    model_form = ServiceTemplateForm

class ServiceTemplateChangeLogView(generic.ObjectChangeLogView):
    base_model = ServiceTemplate

# Service Requirement Views
class ServiceRequirementListView(generic.ObjectListView):
    queryset = ServiceRequirement.objects.all()
    table = ServiceRequirementTable

class ServiceRequirementDetailView(generic.BaseObjectView):
    queryset = ServiceRequirement.objects.all()

class ServiceRequirementEditView(generic.ObjectEditView):
    queryset = ServiceRequirement.objects.all()
    form = ServiceRequirementForm

class ServiceRequirementDeleteView(generic.ObjectDeleteView):
    queryset = ServiceRequirement.objects.all()

class ServiceRequirementBulkImportView(generic.BulkImportView):
    queryset = ServiceRequirement.objects.all()
    model_form = ServiceRequirementForm

class ServiceRequirementChangeLogView(generic.ObjectChangeLogView):
    base_model = ServiceRequirement

# Solution Deployment Views
class SolutionDeploymentListView(generic.ObjectListView):
    queryset = SolutionDeployment.objects.all()
    table = SolutionDeploymentTable

class SolutionDeploymentDetailView(generic.BaseObjectView):
    queryset = SolutionDeployment.objects.all()

class SolutionDeploymentEditView(generic.ObjectEditView):
    queryset = SolutionDeployment.objects.all()
    form = SolutionDeploymentForm

class SolutionDeploymentDeleteView(generic.ObjectDeleteView):
    queryset = SolutionDeployment.objects.all()

class SolutionDeploymentBulkImportView(generic.BulkImportView):
    queryset = SolutionDeployment.objects.all()
    model_form = SolutionDeploymentForm

class SolutionDeploymentChangeLogView(generic.ObjectChangeLogView):
    base_model = SolutionDeployment

# Service Deployment Views
class ServiceDeploymentListView(generic.ObjectListView):
    queryset = ServiceDeployment.objects.all()
    table = ServiceDeploymentTable

class ServiceDeploymentDetailView(generic.BaseObjectView):
    queryset = ServiceDeployment.objects.all()

class ServiceDeploymentEditView(generic.ObjectEditView):
    queryset = ServiceDeployment.objects.all()
    form = ServiceDeploymentForm

class ServiceDeploymentDeleteView(generic.ObjectDeleteView):
    queryset = ServiceDeployment.objects.all()

class ServiceDeploymentBulkImportView(generic.BulkImportView):
    queryset = ServiceDeployment.objects.all()
    model_form = ServiceDeploymentForm

class ServiceDeploymentChangeLogView(generic.ObjectChangeLogView):
    base_model = ServiceDeployment

# Service Component Views
class ServiceComponentListView(generic.ObjectListView):
    queryset = ServiceComponent.objects.all()
    table = ServiceComponentTable

class ServiceComponentDetailView(generic.BaseObjectView):
    queryset = ServiceComponent.objects.all()

class ServiceComponentEditView(generic.ObjectEditView):
    queryset = ServiceComponent.objects.all()
    form = ServiceComponentForm

class ServiceComponentDeleteView(generic.ObjectDeleteView):
    queryset = ServiceComponent.objects.all()

class ServiceComponentBulkImportView(generic.BulkImportView):
    queryset = ServiceComponent.objects.all()
    model_form = ServiceComponentForm

class ServiceComponentChangeLogView(generic.ObjectChangeLogView):
    base_model = ServiceComponent
