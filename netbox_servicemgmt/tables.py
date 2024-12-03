import django_tables2 as tables
from netbox.tables import NetBoxTable
from .models import (
    SLO, SLA, FaultTolerance, SolutionRequest, 
    SolutionTemplate, ServiceTemplate, ServiceRequirement, 
    ServiceDeployment, ServiceComponent
)

class SLOTable(NetBoxTable):
    name = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = SLO
        fields = ('pk', 'name', 'description', 'rpo', 'rto', 'sev1_response', 'sev2_response', 'sev3_response', 'status', 'last_modified', 'created')
        default_columns = ('name', 'rpo', 'rto', 'status')

class SLATable(NetBoxTable):
    name = tables.Column(linkify=True)
    slo = tables.Column(linkify=True)
    business_owner_tenant = tables.Column(linkify=True)
    business_owner_contact = tables.Column(linkify=True)
    technical_contact = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = SLA
        fields = ('pk', 'name', 'description', 'uuid', 'slo', 'business_owner_tenant', 'business_owner_contact', 'technical_contact', 'data_classification', 'status', 'last_modified', 'created')
        default_columns = ('name', 'slo', 'business_owner_tenant', 'data_classification', 'status')

class FaultToleranceTable(NetBoxTable):
    name = tables.Column(linkify=True)
    primary_site = tables.Column(linkify=True)
    secondary_site = tables.Column(linkify=True)
    tertiary_site = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = FaultTolerance
        fields = ('pk', 'name', 'description', 'primary_site', 'secondary_site', 'tertiary_site', 'vip_required', 'clustered', 'multi_site', 'multi_region', 'status', 'last_modified', 'created')
        default_columns = ('name', 'primary_site', 'vip_required', 'clustered', 'status')

class SolutionRequestTable(NetBoxTable):
    name = tables.Column(linkify=True)
    design_contact = tables.Column(linkify=True)
    business_owner_tenant = tables.Column(linkify=True)
    business_owner_contact = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = SolutionRequest
        fields = ('pk', 'name', 'description', 'design_contact', 'business_owner_tenant', 'solution_type', 'status', 'last_modified', 'created')
        default_columns = ('name', 'solution_type', 'design_contact', 'status')

class SolutionTemplateTable(NetBoxTable):
    name = tables.Column(linkify=True)
    design_contact = tables.Column(linkify=True)
    fault_tolerence = tables.Column(linkify=True)
    solution_request = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = SolutionTemplate
        fields = ('pk', 'name', 'description', 'design_contact', 'solution_type', 'fault_tolerence', 'solution_request', 'status', 'last_modified', 'created')
        default_columns = ('name', 'solution_type', 'design_contact', 'status')

class ServiceTemplateTable(NetBoxTable):
    name = tables.Column(linkify=True)
    design_contact = tables.Column(linkify=True)
    fault_tolerence = tables.Column(linkify=True)
    service_slo = tables.Column(linkify=True)
    vendor = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = ServiceTemplate
        fields = ('pk', 'name', 'description', 'design_contact', 'service_type', 'service_slo', 'vendor', 'status', 'last_modified', 'created')
        default_columns = ('name', 'service_type', 'design_contact', 'status')

class ServiceRequirementTable(NetBoxTable):
    name = tables.Column(linkify=True)
    service_template = tables.Column(linkify=True)
    requirement_owner = tables.Column(linkify=True)
    fault_tolerence = tables.Column(linkify=True)
    service_slo = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = ServiceRequirement
        fields = ('pk', 'name', 'description', 'service_template', 'requirement_owner', 'fault_tolerence', 'service_slo', 'status', 'last_modified', 'created')
        default_columns = ('name', 'service_template', 'requirement_owner', 'status')

class ServiceDeploymentTable(NetBoxTable):
    name = tables.Column(linkify=True)
    service_template = tables.Column(linkify=True)
    engineering_contact = tables.Column(linkify=True)
    operations_contact = tables.Column(linkify=True)
    monitoring_contact = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = ServiceDeployment
        fields = ('pk', 'name', 'description', 'service_template', 'engineering_contact', 'operations_contact', 'monitoring_contact', 'status', 'last_modified', 'created')
        default_columns = ('name', 'service_template', 'engineering_contact', 'status')

class ServiceComponentTable(NetBoxTable):
    name = tables.Column(linkify=True)
    service_requirement = tables.Column(linkify=True)
    service_deployment = tables.Column(linkify=True)
    content_object = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = ServiceComponent
        fields = ('pk', 'name', 'description', 'service_requirement', 'service_deployment', 'content_object', 'status', 'last_modified', 'created')
        default_columns = ('name', 'service_requirement', 'service_deployment', 'status')
