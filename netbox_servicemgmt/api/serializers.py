from rest_framework import serializers
from ..models import SLO, FaultTolerence, SolutionBase, Solution, Deployment, Component

class SLOSerializer(serializers.ModelSerializer):
    class Meta:
        model = SLO
        fields = '__all__'

class FaultTolerenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaultTolerence
        fields = '__all__'

class SolutionBaseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SolutionBase
        fields = [
            'name', 'solution_number', 'project_id', 'description', 'solution_type', 'version', 
            'architect', 'requester', 'business_owner_group', 'business_owner_contact',
            'os_technical_contact_group', 'os_technical_contact', 'app_technical_contact_group', 
            'app_technical_contact', 'incident_contact', 'data_classification', 
            'compliance_requirements', 'fault_tolerence', 'slos', 'last_bcdr_test', 
            'last_risk_assessment', 'last_review', 'production_readiness_status', 
            'vendor_management_status', 'status'
        ]

class SolutionSerializer(SolutionBaseSerializer):
    previous_version = serializers.PrimaryKeyRelatedField(
        queryset=Solution.objects.all(),
        allow_null=True,
        required=False
    )
    
    class Meta(SolutionBaseSerializer.Meta):
        model = Solution
        fields = SolutionBaseSerializer.Meta.fields + ['previous_version']

class DeploymentSerializer(SolutionBaseSerializer):
    
    deployment_solution = serializers.PrimaryKeyRelatedField(
        queryset=Solution.objects.all(),
        allow_null=True,
        required=False
    )
    previous_version = serializers.PrimaryKeyRelatedField(
        queryset=Deployment.objects.all(),
        allow_null=True,
        required=False
    )

    class Meta(SolutionBaseSerializer.Meta):
        model = Deployment
        fields = SolutionBaseSerializer.Meta.fields + ['deployment_type', 'deployment_solution', 'previous_version']


class ComponentSerializer(SolutionBaseSerializer):
    content_object = serializers.SerializerMethodField()
    
    def get_content_object(self, obj):
        if obj.content_object:
            return {
                'model': obj.content_object._meta.model_name,
                'id': obj.content_object.id,
                'object': str(obj.content_object)  # or serialize further as needed
            }
        return None