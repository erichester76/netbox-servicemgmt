from netbox.views import generic
from .models import SolutionTemplate, ServiceTemplate, ServiceRequirement, SolutionDeployment, ServiceDeployment, ServiceComponent, HAModel, SLO
from .forms import SolutionTemplateForm, ServiceTemplateForm, ServiceRequirementForm, SolutionDeploymentForm, ServiceDeploymentForm, ServiceComponentForm, HAModelForm, SLOForm
from .tables import SolutionTemplateTable, ServiceTemplateTable, ServiceRequirementTable, SolutionDeploymentTable, ServiceDeploymentTable, ServiceComponentTable, HAModelTable, SLOTable

# SolutionTemplate Views
class SolutionTemplateListView(generic.ObjectListView):
    queryset = SolutionTemplate.objects.all()
    table = SolutionTemplateTable

class SolutionTemplateDetailView(generic.ObjectDetailView):
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
    queryset = SolutionTemplate.objects.all()

# ServiceTemplate Views
class ServiceTemplateListView(generic.ObjectListView):
    queryset = ServiceTemplate.objects.all()
    table = ServiceTemplateTable

class ServiceTemplateDetailView(generic.ObjectDetailView):
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
    queryset = ServiceTemplate.objects.all()

# ServiceRequirement Views
class ServiceRequirementListView(generic.ObjectListView):
    queryset = ServiceRequirement.objects.all()
    table = ServiceRequirementTable

class ServiceRequirementDetailView(generic.ObjectDetailView):
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
    queryset = ServiceRequirement.objects.all()

# SolutionDeployment Views
class SolutionDeploymentListView(generic.ObjectListView):
    queryset = SolutionDeployment.objects.all()
    table = SolutionDeploymentTable

class SolutionDeploymentDetailView(generic.ObjectDetailView):
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
    queryset = SolutionDeployment.objects.all()

# ServiceDeployment Views
class ServiceDeploymentListView(generic.ObjectListView):
    queryset = ServiceDeployment.objects.all()
    table = ServiceDeploymentTable

class ServiceDeploymentDetailView(generic.ObjectDetailView):
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
    queryset = ServiceDeployment.objects.all()

# ServiceComponent Views
class ServiceComponentListView(generic.ObjectListView):
    queryset = ServiceComponent.objects.all()
    table = ServiceComponentTable

class ServiceComponentDetailView(generic.ObjectDetailView):
    queryset = ServiceComponent.objects.all()

class ServiceComponentEditView(generic.ObjectEditView):
    queryset = ServiceComponent.objects.all()

class ServiceComponentDeleteView(generic.ObjectDeleteView):
    queryset = ServiceComponent.objects.all()

class ServiceComponentBulkImportView(generic.BulkImportView):
    queryset = ServiceComponent.objects.all()
    model_form = ServiceComponentForm

class ServiceComponentChangeLogView(generic.bjectChangeLogView):
    queryset = ServiceComponent.objects.all()

# HAModel Views
class HAModelListView(generic.ObjectListView):
    queryset = HAModel.objects.all()
    table = HAModelTable

class HAModelDetailView(generic.ObjectDetailView):
    queryset = HAModel.objects.all()

class HAModelEditView(generic.ObjectEditView):
    queryset = HAModel.objects.all()
    form = HAModelForm

class HAModelDeleteView(generic.ObjectDeleteView):
    queryset = HAModel.objects.all()

class HAModelBulkImportView(generic.BulkImportView):
    queryset = HAModel.objects.all()
    model_form = HAModelForm

class HAModelChangeLogView(generic.ObjectChangeLogView):
    queryset = HAModel.objects.all()

# SLO Views
class SLOListView(generic.ObjectListView):
    queryset = SLO.objects.all()
    table = SLOTable

class SLODetailView(generic.ObjectDetailView):
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
    queryset = SLO.objects.all()
