from django import forms
from .models import SLO, SolutionTemplate, FaultTolerance, ServiceTemplate, ServiceRequirement, SolutionDeployment, ServiceDeployment, ServiceComponent

class SLOForm(forms.ModelForm):
    class Meta:
        model = SLO
        fields = ['name', 'description', 'rpo', 'rto', 'sev1_response', 'sev2_response', 'sev3_response']

class SolutionTemplateForm(forms.ModelForm):
    class Meta:
        model = SolutionTemplate
        fields = ['name', 'description', 'design_contact', 'requirements']

class FaultToleranceForm(forms.ModelForm):
    class Meta:
        model = FaultTolerance
        fields = ['name', 'description', 'vip_required', 'offsite_replication', 'clustered', 'multi_site', 'multi_region', 'snapshots', 'offsite_backup', 'airgap_backup', 'primary_site', 'secondary_site', 'tertiary_site', 'instances_per_site', 'backup_schedule']

class ServiceTemplateForm(forms.ModelForm):
    class Meta:
        model = ServiceTemplate
        fields = ['name', 'description', 'solution_template', 'design_contact', 'service_type', 'vendor_management_assessment', 'vendor', 'fault_tolerence', 'service_slo']

class ServiceRequirementForm(forms.ModelForm):
    class Meta:
        model = ServiceRequirement
        fields = ['name', 'description', 'service_template', 'requirement_owner', 'service_slo', 'vip_required', 'offsite_replication', 'clustered', 'multi_site', 'multi_region', 'snapshots', 'offsite_backup', 'airgap_backup', 'primary_site', 'secondary_site', 'tertiary_site', 'instances_per_site', 'backup_schedule', 'requirement1_field', 'requirement1_value', 'requirement2_field', 'requirement2_value', 'requirement3_field', 'requirement3_value', 'requirement4_field', 'requirement4_value', 'requirement5_field', 'requirement5_value', 'requirement6_field', 'requirement6_value', 'requirement7_field', 'requirement7_value', 'requirement8_field', 'requirement8_value', 'requirement9_field', 'requirement9_value', 'requirement10_field', 'requirement10_value', 'requirement11_field', 'requirement11_value', 'requirement12_field', 'requirement12_value', 'requirement13_field', 'requirement13_value', 'requirement14_field', 'requirement14_value', 'requirement15_field', 'requirement15_value', 'requirement16_field', 'requirement16_value', 'requirement17_field', 'requirement17_value', 'requirement18_field', 'requirement18_value', 'requirement19_field', 'requirement19_value', 'requirement20_field', 'requirement20_value']

class SolutionDeploymentForm(forms.ModelForm):
    class Meta:
        model = SolutionDeployment
        fields = ['name', 'description', 'solution_template', 'deployment_type', 'deployment_date']

class ServiceDeploymentForm(forms.ModelForm):
    class Meta:
        model = ServiceDeployment
        fields = ['name', 'description', 'service_template', 'solution_deployment', 'production_readiness_checklist', 'business_owner_tenant', 'business_owner_contact', 'service_owner_tenant', 'service_owner_contact', 'major_incident_coordinator_contact', 'functional_area_sponsor_tenant', 'functional_sub_area_sponsor_tenant', 'engineering_contact', 'operations_contact', 'monitoring_contact']

class ServiceComponentForm(forms.ModelForm):
    class Meta:
        model = ServiceComponent
        fields = ['name', 'description', 'service_deployment', 'service_requirement', 'object_type', 'object_id']
