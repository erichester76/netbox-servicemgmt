from django import forms
from .models import SolutionTemplate, ServiceTemplate, ServiceRequirement, SolutionDeployment, ServiceDeployment, ServiceComponent, HAModel, SLO

class SolutionTemplateForm(forms.ModelForm):
    class Meta:
        model = SolutionTemplate
        fields = ['name', 'description', 'architect_contact', 'problem_statement', 'business_requirements', 'budget']

class ServiceTemplateForm(forms.ModelForm):
    class Meta:
        model = ServiceTemplate
        fields = ['name', 'solution_template', 'responsible_design', 'responsible_deployment', 'responsible_operations', 'responsible_monitoring']

class ServiceRequirementForm(forms.ModelForm):
    class Meta:
        model = ServiceRequirement
        fields = ['service_template', 'requirement1', 'requirement2', 'requirement3', 'requirement20', 'object_type']

class SolutionDeploymentForm(forms.ModelForm):
    class Meta:
        model = SolutionDeployment
        fields = ['solution_template', 'tenant', 'deployment_date']

class ServiceDeploymentForm(forms.ModelForm):
    class Meta:
        model = ServiceDeployment
        fields = ['service_template', 'solution_deployment']

class ServiceComponentForm(forms.ModelForm):
    class Meta:
        model = ServiceComponent
        fields = ['service_deployment', 'object_type', 'object_id']

class HAModelForm(forms.ModelForm):
    class Meta:
        model = HAModel
        fields = ['service_template', 'vip_required', 'primary_site', 'secondary_site', 'tertiary_site', 'replication', 'cluster', 'multi_site', 'snapshots']

class SLOForm(forms.ModelForm):
    class Meta:
        model = SLO
        fields = ['service_template', 'rpo', 'rto', 'sev1_response', 'sev2_response', 'replicas_per_site']
