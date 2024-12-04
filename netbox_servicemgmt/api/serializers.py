from netbox.api.serializers import NetBoxModelSerializer
from ..models import (
    SLO, SLA, FaultTolerence, SolutionRequest, 
    SolutionTemplate, ServiceTemplate, ServiceRequirement, 
    ServiceDeployment, ServiceComponent
)

class SLOSerializer(NetBoxModelSerializer):
    class Meta:
        model = SLO
        fields = '__all__'

class SLASerializer(NetBoxModelSerializer):
    class Meta:
        model = SLA
        fields = '__all__'

class FaultTolerenceSerializer(NetBoxModelSerializer):
    class Meta:
        model = FaultTolerence
        fields = '__all__'

class SolutionRequestSerializer(NetBoxModelSerializer):
    class Meta:
        model = SolutionRequest
        fields = '__all__'

class SolutionTemplateSerializer(NetBoxModelSerializer):
    class Meta:
        model = SolutionTemplate
        fields = '__all__'

class ServiceTemplateSerializer(NetBoxModelSerializer):
    class Meta:
        model = ServiceTemplate
        fields = '__all__'

class ServiceRequirementSerializer(NetBoxModelSerializer):
    class Meta:
        model = ServiceRequirement
        fields = '__all__'

class ServiceDeploymentSerializer(NetBoxModelSerializer):
    class Meta:
        model = ServiceDeployment
        fields = '__all__'

class ServiceComponentSerializer(NetBoxModelSerializer):
    class Meta:
        model = ServiceComponent
        fields = '__all__'
