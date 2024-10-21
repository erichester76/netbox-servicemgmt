from netbox.api.serializers import NetBoxModelSerializer, WritableNestedSerializer
from ..models import SLO, SolutionTemplate, FaultTolerance, ServiceTemplate, ServiceRequirement, ServiceDeployment, ServiceComponent

class SLOSerializer(NetBoxModelSerializer):
    class Meta:
        model = SLO
        fields = ['id', 'name', 'description', 'rpo', 'rto', 'sev1_response', 'sev2_response', 'sev3_response']

class SolutionTemplateSerializer(NetBoxModelSerializer):
    class Meta:
        model = SolutionTemplate
        fields = ['id', 'name', 'description', 'version', 'design_contact', 'business_owner_contact', 'business_owner_tenant', 'solution_type', 'requirements']

class FaultToleranceSerializer(NetBoxModelSerializer):
    class Meta:
        model = FaultTolerance
        fields = ['id', 'name', 'description', 'vip_required', 'offsite_replication', 'clustered', 'multi_site', 'multi_region', 'snapshots', 'offsite_backup', 'airgap_backup', 'primary_site', 'secondary_site', 'tertiary_site', 'instances_per_site', 'backup_schedule']

class ServiceTemplateSerializer(NetBoxModelSerializer):
    class Meta:
        model = ServiceTemplate
        fields = ['id','name', 'description', 'version', 'solution_templates', 'design_contact', 'service_type', 'vendor_management_assessment', 'vendor', 'fault_tolerence', 'service_slo']

class ServiceRequirementSerializer(NetBoxModelSerializer):
    class Meta:
        model = ServiceRequirement
        fields = [
            'id', 'name', 'description', 'service_template', 'requirement_owner', 'service_slo',
            'primary_site', 'secondary_site', 'tertiary_site', 'instances_per_site', 'vip_required',
            'offsite_replication', 'clustered', 'multi_site', 'multi_region', 'snapshots', 'backup_schedule',
            'offsite_backup', 'airgap_backup', 'object_type'
        ]
class ServiceDeploymentSerializer(NetBoxModelSerializer):
    class Meta:
        model = ServiceDeployment
        fields = ['id', 'name', 'description', 'version', 'service_template', 'deployment_rfc', 'maintenance_window', 'production_readiness_checklist', 'business_owner_tenant', 'business_owner_contact', 'service_owner_tenant', 'service_owner_contact', 'major_incident_coordinator_contact', 'functional_area_sponsor_tenant', 'functional_sub_area_sponsor_tenant', 'engineering_contact', 'operations_contact', 'monitoring_contact']

class ServiceComponentSerializer(NetBoxModelSerializer):
    class Meta:
        model = ServiceComponent
        fields = ['id', 'name', 'description', 'version', 'service_deployment', 'service_requirement', 'object_type', 'object_id']
