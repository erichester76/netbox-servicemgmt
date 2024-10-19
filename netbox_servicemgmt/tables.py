import django_tables2 as tables
from netbox.tables import NetBoxTable
from .models import SLO, SolutionTemplate, FaultTolerence, ServiceTemplate, ServiceRequirement, SolutionDeployment, ServiceDeployment, ServiceComponent

class SLOTable(NetBoxTable):
    name = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = SLO
        fields = ('name', 'description', 'rpo', 'rto', 'sev1_response', 'sev2_response')

class SolutionTemplateTable(NetBoxTable):
    name = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = SolutionTemplate
        fields = ('name', 'description', 'design_contact')

class FaultTolerenceTable(NetBoxTable):
    name = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = FaultTolerence
        fields = ('name', 'description', 'service_template', 'primary_site', 'secondary_site', 'tertiary_site', 'instances_per_site')

class ServiceTemplateTable(NetBoxTable):
    name = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = ServiceTemplate
        fields = ('name', 'description', 'solution_template', 'design_contact', 'service_type', 'vendor')

class ServiceRequirementTable(NetBoxTable):
    name = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = ServiceRequirement
        fields = ('name', 'description', 'service_template', 'requirement_owner', 'service_slo', 'primary_site', 'secondary_site')

class SolutionDeploymentTable(NetBoxTable):
    name = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = SolutionDeployment
        fields = ('name', 'description', 'solution_template', 'deployment_type', 'deployment_date')

class ServiceDeploymentTable(NetBoxTable):
    name = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = ServiceDeployment
        fields = ('name', 'description', 'service_template', 'solution_deployment', 'business_owner_tenant', 'service_owner_tenant')

class ServiceComponentTable(NetBoxTable):
    name = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = ServiceComponent
        fields = ('name', 'description', 'service_deployment', 'service_requirement', 'content_object')
