from netbox.api.serializers import NetBoxModelSerializer
from ..models import (
    Solution, SLO, FaultTolerence,
    Deployment, Component
)

class SLOSerializer(NetBoxModelSerializer):
    class Meta:
        model = SLO
        fields = '__all__'

class FaultTolerenceSerializer(NetBoxModelSerializer):
    class Meta:
        model = FaultTolerence
        fields = '__all__'

class SolutionSerializer(NetBoxModelSerializer):
    class Meta:
        model = Solution
        fields = '__all__'


class DeploymentSerializer(NetBoxModelSerializer):
    class Meta:
        model = Deployment
        fields = '__all__'

class ComponentSerializer(NetBoxModelSerializer):
    class Meta:
        model = Component
        fields = '__all__'
