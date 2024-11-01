import django_tables2 as tables
from netbox.tables import NetBoxTable
from . import models

class SLOTable(NetBoxTable):
    name = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = models.SLO
        default_columns = ('name', 'description', 'rpo', 'rto', 'sev1_response', 'sev2_response', 'sev3_reponse')
        fields = ('pk', 'id', 'name', 'description', 'rpo', 'rto', 'sev1_response', 'sev2_response', 'sev3_reponse')
    
class SLATable(NetBoxTable):
    name = tables.Column(linkify=True)
    slo = tables.Column(linkify=True)
    business_owner_contact = tables.Column(linkify=True)
    businss_owner_tenant = tables.Column(linkify=True)
    technical_contact = tables.Column(linkify=True)
    
    class Meta(NetBoxTable.Meta):
        model = models.SLA 
        default_columns = ('name', 'description', 'slo', 'business_owner_contact', 'business_owner_tenant', 'technical_contact', 'data_classification' )
        fields = ( 'pk', 'id', 'uuid', 'name', 'description', 'slo', 'business_owner_contact', 'business_owner_tenant', 'technical_contact', 'data_classification' )

class SolutionRequestTable(NetBoxTable):
    name = tables.Column(linkify=True)
    design_contact = tables.Column(linkify=True)
    business_owner_contact = tables.Column(linkify=True)
    business_owner_tenant = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model =models.SolutionRequest
        default_columns = ('name', 'version', 'solution_type', 'business_owner_contact', 'business_owner_tenant', 'design_contact')
        fields = ('pk', 'id', 'name', 'description', 'version', 'design_contact', 'business_owner_contact', 'business_owner_tenant', 'solution_type', 'requirements')
        
class SolutionTemplateTable(NetBoxTable):
    name = tables.Column(linkify=True)
    design_contact = tables.Column(linkify=True)
    business_owner_contact = tables.Column(linkify=True)
    business_owner_tenant = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = models.SolutionTemplate
        default_columns = ('name', 'version', 'solution_type', 'business_owner_contact', 'business_owner_tenant', 'design_contact')
        fields = ('pk', 'id', 'name', 'description', 'version', 'design_contact', 'business_owner_contact', 'business_owner_tenant', 'solution_type', 'requirements')

class FaultToleranceTable(NetBoxTable):
    name = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = models.FaultTolerance
        default_columns = ('name', 'description', 'primary_site', 'secondary_site', 'tertiary_site')
        fields = ('pk', 'id', 'name', 'description', 'vip_required', 'offsite_replication', 'clustered', 'multi_site', 'multi_region', 'snapshots', 'offsite_backup', 'airgap_backup', 'primary_site', 'secondary_site', 'tertiary_site', 'instances_per_site', 'backup_schedule')

class ServiceTemplateTable(NetBoxTable):
    name = tables.Column(linkify=True)
    solution_template = tables.Column(linkify=True)
    fault_tolerence = tables.Column(linkify=True)
    service_slo = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = models.ServiceTemplate
        default_columns = ('name', 'description', 'version', 'service_type', 'fault_tolerence', 'service_slo')
        fields = ('pk', 'id', 'name', 'description', 'version', 'solution_templates', 'design_contact', 'service_type', 'vendor_management_assessment', 'vendor', 'fault_tolerence', 'service_slo')

class ServiceRequirementTable(NetBoxTable):
    name = tables.Column(linkify=True)
    requirement_owner = tables.Column(linkify=True)
    service_slo = tables.Column(linkify=True)
    service_template = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = models.ServiceRequirement
        default_columns = ('name', 'description', 'version', 'service_template', 'requirement_owner', 'service_slo')
        fields = ('pk', 'id', 'name', 'description', 'version', 'service_template', 'requirement_owner', 'service_slo',
            'primary_site', 'secondary_site', 'tertiary_site', 'instances_per_site', 'vip_required',
            'offsite_replication', 'clustered', 'multi_site', 'multi_region', 'snapshots', 'backup_schedule',
            'offsite_backup', 'airgap_backup', 'object_type'
        )
        
class ServiceDeploymentTable(NetBoxTable):
    name = tables.Column(linkify=True)
    service_template = tables.Column(linkify=True)
    business_owner_tenant = tables.Column(linkify=True)
    service_owner_tenant = tables.Column(linkify=True)
    
    class Meta(NetBoxTable.Meta):
        model = models.ServiceDeployment
        default_columns = ('name', 'description', 'version', 'service_template', 'business_owner_tenant', 'service_owner_tenant')
        fields = ('pk', 'id', 'name', 'description', 'version', 'service_template', 'production_readiness_checklist', 'business_owner_tenant', 'business_owner_contact', 'service_owner_tenant', 'service_owner_contact', 'major_incident_coordinator_contact', 'functional_area_sponsor_tenant', 'functional_sub_area_sponsor_tenant', 'engineering_contact', 'operations_contact', 'monitoring_contact')

class ServiceComponentTable(NetBoxTable):
    name = tables.Column(linkify=True)
    service_deployment = tables.Column(linkify=True)
    content_object = tables.Column(linkify=True)
    service_deployment = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = models.ServiceComponent
        default_columns = ('name', 'description', 'version', 'service_deployment', 'service_requirement', 'content_object')
        fields = ('pk', 'id', 'name', 'description', 'version', 'service_deployment', 'service_requirement', 'object_type', 'object_id')

