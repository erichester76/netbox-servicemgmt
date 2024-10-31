from netbox.api.serializers import NetBoxModelSerializer, WritableNestedSerializer
from .. import models

class SLOSerializer(NetBoxModelSerializer):
    class Meta:
        model = models.SLO
        fields = ['id', 'name', 'description', 'rpo', 'rto', 'sev1_response', 'sev2_response', 'sev3_response']

class SLASerializer(NetBoxModelSerializer):
    class Meta:
        model = models.SLA
        fields = ['id', 'name', 'description', 'slo', 'business_owner_contact', 'business_owner_tenant', 'technical_contact', 'data_classification' ]


class SolutionTemplateSerializer(NetBoxModelSerializer):
    class Meta:
        model = models.SolutionTemplate
        fields = ['id', 'name', 'description', 'version', 'design_contact', 'business_owner_contact', 'business_owner_tenant', 'solution_type', 'requirements']

class SolutionRequestSerializer(NetBoxModelSerializer):
    class Meta:
        model = models.SolutionRequest
        fields = ['id', 'name', 'description', 'version', 'design_contact', 'business_owner_contact', 'business_owner_tenant', 'solution_type', 'requirements']

class FaultToleranceSerializer(NetBoxModelSerializer):
    class Meta:
        model = models.FaultTolerance
        fields = ['id', 'name', 'description', 'vip_required', 'offsite_replication', 'clustered', 'multi_site', 'multi_region', 'snapshots', 'offsite_backup', 'airgap_backup', 'primary_site', 'secondary_site', 'tertiary_site', 'instances_per_site', 'backup_schedule']

class ServiceTemplateSerializer(NetBoxModelSerializer):
    class Meta:
        model = models.ServiceTemplate
        fields = ['id', 'name', 'description', 'version', 'solution_templates', 'design_contact', 'service_type', 'vendor_management_assessment', 'vendor', 'fault_tolerence', 'service_slo']

class ServiceRequirementSerializer(NetBoxModelSerializer):
    class Meta:
        model = models.ServiceRequirement
        fields = [
            'id', 'name', 'description', 'service_template', 'requirement_owner', 'service_slo',
            'primary_site', 'secondary_site', 'tertiary_site', 'instances_per_site', 'vip_required',
            'offsite_replication', 'clustered', 'multi_site', 'multi_region', 'snapshots', 'backup_schedule',
            'offsite_backup', 'airgap_backup', 'object_type'
        ]
        
class ServiceDeploymentSerializer(NetBoxModelSerializer):
    class Meta:
        model = models.ServiceDeployment
        fields = ['id', 'name', 'description', 'version', 'service_template', 'deployment_rfc', 'maintenance_window', 'production_readiness_checklist', 'business_owner_tenant', 'business_owner_contact', 'service_owner_tenant', 'service_owner_contact', 'major_incident_coordinator_contact', 'functional_area_sponsor_tenant', 'functional_sub_area_sponsor_tenant', 'engineering_contact', 'operations_contact', 'monitoring_contact']

class ServiceComponentSerializer(NetBoxModelSerializer):
    class Meta:
        model = models.ServiceComponent
        fields = ['id', 'name', 'description', 'version', 'service_deployment', 'service_requirement', 'object_type', 'object_id']
