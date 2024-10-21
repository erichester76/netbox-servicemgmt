import django_tables2 as tables
from netbox.tables import NetBoxTable
from .models import SLO, SolutionTemplate, FaultTolerance, ServiceTemplate, ServiceRequirement, SolutionDeployment, ServiceDeployment, ServiceComponent

class SLOTable(NetBoxTable):
    name = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = SLO
        fields = ('name', 'description', 'rpo', 'rto', 'sev1_response', 'sev2_response', 'sev3_reponse')

class SolutionTemplateTable(NetBoxTable):
    name = tables.Column(linkify=True)
    design_contact = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = SolutionTemplate
        fields = ('name', 'description', 'design_contact')

class FaultToleranceTable(NetBoxTable):
    name = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = FaultTolerance
        fields = ('name', 'description', 'primary_site', 'secondary_site', 'tertiary_site')
        
class ServiceTemplateTable(NetBoxTable):
    name = tables.Column(linkify=True)
    solution_template = tables.Column(linkify=True)
    fault_tolerence = tables.Column(linkify=True)
    service_slo = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = ServiceTemplate
        fields = ('name', 'description', 'service_type', 'fault_tolerence', 'service_slo')

class ServiceRequirementTable(NetBoxTable):
    name = tables.Column(linkify=True)
    solution_template = tables.Column(linkify=True)
    requirement_owner = tables.Column(linkify=True)
    service_slo = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = ServiceRequirement
        fields = ('name', 'description', 'service_template', 'requirement_owner', 'service_slo')

class SolutionDeploymentTable(NetBoxTable):
    name = tables.Column(linkify=True)
    solution_template = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = SolutionDeployment
        fields = ('name', 'description', 'solution_template', 'deployment_type', 'deployment_date')

class ServiceDeploymentTable(NetBoxTable):
    name = tables.Column(linkify=True)
    service_template = tables.Column(linkify=True)
    solution_deployment = tables.Column(linkify=True)
    business_owner_tenant = tables.Column(linkify=True)
    service_owner_tenant = tables.Column(linkify=True)
    
    class Meta(NetBoxTable.Meta):
        model = ServiceDeployment
        fields = ('name', 'description', 'service_template', 'solution_deployment', 'business_owner_tenant', 'service_owner_tenant')

class ServiceComponentTable(NetBoxTable):
    name = tables.Column(linkify=True)
    service_deployment = tables.Column(linkify=True)
    content_object = tables.Column(linkify=True)
    service_deployment = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = ServiceComponent
        fields = ('name', 'description', 'service_deployment', 'service_requirement', 'content_object')
