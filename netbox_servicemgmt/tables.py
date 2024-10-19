import django_tables2 as tables
from netbox.tables import NetBoxTable
from .models import SolutionTemplate, ServiceTemplate, ServiceRequirement, SolutionDeployment, ServiceDeployment, ServiceComponent, HAModel, SLO

class SolutionTemplateTable(NetBoxTable):
    name = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = SolutionTemplate
        fields = ('name', 'description', 'architect_contact', 'problem_statement', 'budget')

class ServiceTemplateTable(NetBoxTable):
    name = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = ServiceTemplate
        fields = ('name', 'solution_template', 'responsible_design', 'responsible_deployment', 'responsible_operations', 'responsible_monitoring')

class ServiceRequirementTable(NetBoxTable):
    service_template = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = ServiceRequirement
        fields = ('service_template', 'requirement1', 'requirement2', 'requirement3', 'requirement20')

class SolutionDeploymentTable(NetBoxTable):
    solution_template = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = SolutionDeployment
        fields = ('solution_template', 'tenant', 'deployment_date')

class ServiceDeploymentTable(NetBoxTable):
    service_template = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = ServiceDeployment
        fields = ('service_template', 'solution_deployment')

class ServiceComponentTable(NetBoxTable):
    service_deployment = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = ServiceComponent
        fields = ('service_deployment', 'content_object')

class HAModelTable(NetBoxTable):
    service_template = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = HAModel
        fields = ('service_template', 'primary_site', 'secondary_site', 'tertiary_site', 'replication', 'cluster', 'multi_site', 'snapshots')

class SLOTable(NetBoxTable):
    service_template = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = SLO
        fields = ('service_template', 'rpo', 'rto', 'sev1_response', 'sev2_response', 'replicas_per_site')
