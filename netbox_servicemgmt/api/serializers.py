from netbox.api.serializers import NetBoxModelSerializer, WritableNestedSerializer
from ..models import SLO, SolutionTemplate, FaultTolerance, ServiceTemplate, ServiceRequirement, SolutionDeployment, ServiceDeployment, ServiceComponent

class SLOSerializer(NetBoxModelSerializer):
    class Meta:
        model = SLO
        fields = ['id', 'name', 'description', 'rpo', 'rto', 'sev1_response', 'sev2_response', 'sev3_response']

class SolutionTemplateSerializer(NetBoxModelSerializer):
    class Meta:
        model = SolutionTemplate
        fields = ['id', 'name', 'description', 'design_contact', 'requirements']

class FaultToleranceSerializer(NetBoxModelSerializer):
    class Meta:
        model = FaultTolerance
        fields = ['id', 'name', 'description', 'vip_required', 'primary_site', 'secondary_site', 'tertiary_site', 'instances_per_site']

class ServiceTemplateSerializer(NetBoxModelSerializer):
    class Meta:
        model = ServiceTemplate
        fields = ['id', 'name', 'description', 'solution_template', 'design_contact', 'service_type', 'vendor_management_assessment', 'vendor', 'fault_tolerence', 'service_slo']

class ServiceRequirementSerializer(NetBoxModelSerializer):
    class Meta:
        model = ServiceRequirement
        fields = ['id', 'name', 'description', 'service_template', 'requirement_owner', 'service_slo', 'primary_site', 'secondary_site', 'requirement1_field', 'requirement1_value', 'requirement2_field', 'requirement2_value', 'requirement3_field', 'requirement3_value']

class SolutionDeploymentSerializer(NetBoxModelSerializer):
    class Meta:
        model = SolutionDeployment
        fields = ['id', 'name', 'description', 'solution_template', 'deployment_type', 'deployment_date']

class ServiceDeploymentSerializer(NetBoxModelSerializer):
    class Meta:
        model = ServiceDeployment
        fields = ['id', 'name', 'description', 'service_template', 'solution_deployment', 'business_owner_tenant', 'service_owner_tenant']

class ServiceComponentSerializer(NetBoxModelSerializer):
    class Meta:
        model = ServiceComponent
        fields = ['id', 'name', 'description', 'service_deployment', 'service_requirement', 'content_object']
