from rest_framework import serializers
from ..models import SolutionTemplate, ServiceTemplate, ServiceRequirement, SolutionDeployment, ServiceDeployment, ServiceComponent, HAModel, SLO

class SolutionTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolutionTemplate
        fields = ['id', 'name', 'description', 'architect_contact', 'problem_statement', 'business_requirements', 'budget']

class ServiceTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceTemplate
        fields = ['id', 'name', 'solution_template', 'responsible_design', 'responsible_deployment', 'responsible_operations', 'responsible_monitoring']

class ServiceRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRequirement
        fields = ['id', 'service_template', 'requirement1', 'requirement2', 'requirement3', 'requirement20', 'object_type']

class SolutionDeploymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolutionDeployment
        fields = ['id', 'solution_template', 'tenant', 'deployment_date']

class ServiceDeploymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceDeployment
        fields = ['id', 'service_template', 'solution_deployment']

class ServiceComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceComponent
        fields = ['id', 'service_deployment', 'object_type', 'object_id', 'content_object']

class HAModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = HAModel
        fields = ['id', 'service_template', 'vip_required', 'primary_site', 'secondary_site', 'tertiary_site', 'replication', 'cluster', 'multi_site', 'snapshots']

class SLOSerializer(serializers.ModelSerializer):
    class Meta:
        model = SLO
        fields = ['id', 'service_template', 'rpo', 'rto', 'sev1_response', 'sev2_response', 'replicas_per_site']
