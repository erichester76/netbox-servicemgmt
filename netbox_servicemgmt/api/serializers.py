from rest_framework import serializers
from ..models import SLO, FaultTolerence, Solution, Deployment, Component

class SLOSerializer(serializers.ModelSerializer):
    class Meta:
        model = SLO
        fields = '__all__'

class FaultTolerenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaultTolerence
        fields = '__all__'

class SolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solution
        fields = '__all__'

class DeploymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Deployment
        fields = '__all__'


class ComponentSerializer(serializers.ModelSerializer):
    content_object = serializers.SerializerMethodField()
    
    def get_content_object(self, obj):
        if obj.content_object:
            return {
                'model': obj.content_object._meta.model_name,
                'id': obj.content_object.id,
                'object': str(obj.content_object)  # or serialize further as needed
            }
        return None