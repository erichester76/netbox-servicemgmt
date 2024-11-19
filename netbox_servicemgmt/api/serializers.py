from netbox.api.serializers import NetBoxModelSerializer
from .. import models

class SLOSerializer(NetBoxModelSerializer):
    class Meta:
        model = models.SLO
        fields = [ 'pk', 'id', 'name', 'description', 'rpo', 'rto', 'sev1_response', 'sev2_response', 'sev3_response' ]

class SLASerializer(NetBoxModelSerializer):
    class Meta:
        model = models.SLA
        fields = [ 'pk', 'id', 'name', 'uuid', 'description', 'slo', 'business_owner_contact', 
                   'business_owner_tenant', 'technical_contact', 'data_classification' ]

class SolutionTemplateSerializer(NetBoxModelSerializer):
    class Meta:
        model = models.SolutionTemplate
        fields = [ 'pk', 'id', 'name', 'description', 'status', 'version', 'solution_request', 'solution_type', 'design_contact', 
                   'slo', 'fault_tolerence', 'data_classification', 'sla_number', 'vendors' ]
        
class SolutionRequestSerializer(NetBoxModelSerializer):
    class Meta:
        model = models.SolutionRequest
        fields = [ 'pk', 'id', 'name', 'description', 'status', 'version', 'solution_type', 'design_contact', 'business_owner_contact', 
                   'business_owner_tenant', 'service_owner_tenant', 'service_owner_contact', 'functional_area_sponsor_tenant', 
                   'functional_sub_area_sponsor_tenant', 'rfp_status', 'rfp_ref', 'slo', 'data_classification', 'clustered', 'multi_site', 
                   'multi_region', 'offsite_backup', 'airgap_backup', 'requirements' ]
        
class FaultToleranceSerializer(NetBoxModelSerializer):
    class Meta:
        model = models.FaultTolerance
        fields = [ 'pk', 'id', 'name', 'description', 'vip_required', 'offsite_replication', 'clustered', 'multi_site', 
                   'multi_region', 'snapshots', 'offsite_backup', 'airgap_backup', 'primary_site', 'secondary_site', 
                   'tertiary_site', 'instances_per_site', 'backup_schedule' ]

class ServiceTemplateSerializer(NetBoxModelSerializer):
    class Meta:
        model = models.ServiceTemplate
        fields = [ 'pk', 'id', 'name', 'description', 'status', 'version', 'solution_templates', 'design_contact', 'service_type', 'vendor', 
                   'vendor_management_number', 'vendor_management_status', 'fault_tolerence', 'service_slo' ]
        
class ServiceRequirementSerializer(NetBoxModelSerializer):
    class Meta:
        model = models.ServiceRequirement
        fields = [ 'pk', 'id', 'name', 'description', 'status', 'service_template', 'requirement_owner', 'service_slo' ]
        
class ServiceDeploymentSerializer(NetBoxModelSerializer):
    class Meta:
        model = models.ServiceDeployment
        fields = [ 'pk', 'id', 'name', 'description', 'status', 'version', 'service_template', 'deployment_rfc', 'maintenance_window', 
                  'production_readiness_checklist', 'major_incident_coordinator_contact', 'engineering_contact', 
                  'operations_contact', 'monitoring_contact' ]

class ServiceComponentSerializer(NetBoxModelSerializer):
    class Meta:
        model = models.ServiceComponent
        fields = ['pk', 'id', 'name', 'description', 'status', 'version', 'service_deployment', 'service_requirement', 'content_type', 'object_id', 'content_object' ]
