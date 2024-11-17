from netbox.forms import NetBoxModelForm, NetBoxModelImportForm
from . import models
from django import forms
from django.contrib.contenttypes.models import ContentType
from dcim.models import Device
from virtualization.models import VirtualMachine

class AttachForm(forms.Form):
    existing_object = forms.ModelChoiceField(
        queryset=None,  # This will be dynamically populated
        label="Select an existing object to attach"
    )

    def __init__(self, *args, **kwargs):
        current_object = kwargs.pop('current_object')
        related_model_class = kwargs.pop('related_model_class')
        super().__init__(*args, **kwargs)

        # Populate the queryset for `existing_object`, excluding the ones already related
        self.fields['existing_object'].queryset = related_model_class.objects.exclude(pk=current_object.pk)
        
class SLOForm(NetBoxModelForm):
    class Meta:
        model = models.SLO
        fields = ['name', 'description', 'rpo', 'rto', 'sev1_response', 'sev2_response', 'sev3_response']

class SLOImportForm(NetBoxModelImportForm):
    class Meta:
        model = models.SLO
        fields = ['name', 'description', 'rpo', 'rto', 'sev1_response', 'sev2_response', 'sev3_response']

class SLAForm(NetBoxModelForm):
    class Meta:
        model = models.SLA
        virtual_machines = forms.ModelMultipleChoiceField(
            queryset=VirtualMachine.objects.all(),
            required=False
        )
        fields = ['name', 'uuid', 'description', 'slo', 'business_owner_contact', 'business_owner_tenant', 'technical_contact', 'data_classification', 'virtual_machines' ]

class SLAImportForm(NetBoxModelImportForm):
    class Meta:
        model = models.SLA
        fields = ['name', 'description', 'slo', 'business_owner_contact', 'business_owner_tenant', 'technical_contact', 'data_classification' ]


class SolutionRequestForm(NetBoxModelForm):
    class Meta:
        model = models.SolutionRequest
        fields = ['name', 'description', 'version', 'solution_type', 'design_contact', 'business_owner_contact', 'business_owner_tenant', 
                'service_owner_tenant', 'service_owner_contact', 'major_incident_coordinator_contact', 'functional_area_sponsor_tenant', 
                'functional_sub_area_sponsor_tenant', 'data_classification', 'rfp_status', 'rfp_ref', 'clustered', 'multi_site', 
                'slo', 'multi_region', 'snapshots', 'offsite_backup', 'airgap_backup', 'requirements']        
class SolutionRequestImportForm(NetBoxModelImportForm):
    class Meta:
        model = models.SolutionRequest
        fields = ['name', 'description', 'version', 'solution_type', 'design_contact', 'business_owner_contact', 'business_owner_tenant', 
                'service_owner_tenant', 'service_owner_contact', 'major_incident_coordinator_contact', 'functional_area_sponsor_tenant', 
                'functional_sub_area_sponsor_tenant', 'data_classification', 'rfp_status', 'rfp_ref', 'clustered', 'multi_site', 
                'slo', 'multi_region', 'snapshots', 'offsite_backup', 'airgap_backup', 'requirements']

class SolutionTemplateForm(NetBoxModelForm):
    class Meta:
        model = models.SolutionTemplate
        fields = ['name', 'description', 'version', 'service_request', 'solution_type', 'design_contact', 'business_owner_contact', 'business_owner_tenant', 
                'service_owner_tenant', 'service_owner_contact', 'major_incident_coordinator_contact', 'functional_area_sponsor_tenant', 
                'functional_sub_area_sponsor_tenant', 'slo', 'fault_tolerence', 'data_classification', 'sla_number', 'vendors', 
                'vendor_management_number', 'vendor_management_status']
               
        
class SolutionTemplateImportForm(NetBoxModelImportForm):
    class Meta:
        model = models.SolutionTemplate
        fields = ['name', 'description', 'version', 'service_request', 'solution_type', 'design_contact', 'business_owner_contact', 'business_owner_tenant', 
                'service_owner_tenant', 'service_owner_contact', 'major_incident_coordinator_contact', 'functional_area_sponsor_tenant', 
                'functional_sub_area_sponsor_tenant', 'slo', 'fault_tolerence', 'data_classification', 'sla_number', 'vendors', 
                'vendor_management_number', 'vendor_management_status']
        
class FaultToleranceForm(NetBoxModelForm):
    class Meta:
        model = models.FaultTolerance
        fields = ['name', 'description', 'vip_required', 'offsite_replication', 'clustered', 'multi_site', 
                  'multi_region', 'snapshots', 'offsite_backup', 'airgap_backup', 'primary_site', 'secondary_site', 
                  'tertiary_site', 'instances_per_site', 'backup_schedule']

class FaultToleranceImportForm(NetBoxModelImportForm):
    class Meta:
        model = models.FaultTolerance
        fields = ['name', 'description', 'vip_required', 'offsite_replication', 'clustered', 'multi_site', 
                  'multi_region', 'snapshots', 'offsite_backup', 'airgap_backup', 'primary_site', 'secondary_site', 
                  'tertiary_site', 'instances_per_site', 'backup_schedule']

class ServiceTemplateForm(NetBoxModelForm):
    class Meta:
        model = models.ServiceTemplate
        fields = ['name', 'description', 'version', 'solution_templates', 'design_contact', 'service_type', 
                  'vendor_management_assessment', 'vendor', 'fault_tolerence', 'service_slo']

class ServiceTemplateImportForm(NetBoxModelImportForm):
    class Meta:
        model = models.ServiceTemplate
        fields = ['name', 'description', 'version', 'solution_templates', 'design_contact', 'service_type', 
                  'vendor_management_assessment', 'vendor', 'fault_tolerence', 'service_slo']


class ServiceRequirementForm(NetBoxModelForm):
    
    class Meta:
        model = models.ServiceRequirement
        fields = ['name', 'description', 'service_template', 'requirement_owner', 'service_slo', 'object_type']

    # Dynamically add requirement fields
    requirement_fields = [
        ('requirement1_field', 'requirement1_value'),
        ('requirement2_field', 'requirement2_value'),
        ('requirement3_field', 'requirement3_value'),
        ('requirement4_field', 'requirement4_value'),
        ('requirement5_field', 'requirement5_value'),
        ('requirement6_field', 'requirement6_value'),
        ('requirement7_field', 'requirement7_value'),
        ('requirement8_field', 'requirement8_value'),
        ('requirement9_field', 'requirement9_value'),
        ('requirement10_field', 'requirement10_value'),
        ('requirement11_field', 'requirement11_value'),
        ('requirement12_field', 'requirement12_value'),
        ('requirement13_field', 'requirement13_value'),
        ('requirement14_field', 'requirement14_value'),
        ('requirement15_field', 'requirement15_value'),
        ('requirement16_field', 'requirement16_value'),
        ('requirement17_field', 'requirement17_value'),
        ('requirement18_field', 'requirement18_value'),
        ('requirement19_field', 'requirement19_value'),
        ('requirement20_field', 'requirement20_value'),
    ]

class ServiceRequirementImportForm(NetBoxModelImportForm):
    
    class Meta:
        model = models.ServiceRequirement
        fields = [
            'name', 'description', 'service_template', 'requirement_owner', 'service_slo',
            'primary_site', 'secondary_site', 'tertiary_site', 'instances_per_site', 'vip_required',
            'offsite_replication', 'clustered', 'multi_site', 'multi_region', 'snapshots', 'backup_schedule',
            'offsite_backup', 'airgap_backup', 'object_type'
        ]
        
class ServiceDeploymentForm(NetBoxModelForm):
    class Meta:
        model = models.ServiceDeployment
        fields = ['name', 'description', 'version', 'service_template', 'deployment_rfc', 'maintenance_window', 
                  'production_readiness_checklist', 'business_owner_tenant', 'business_owner_contact', 'service_owner_tenant', 
                  'service_owner_contact', 'major_incident_coordinator_contact', 'functional_area_sponsor_tenant', 
                  'functional_sub_area_sponsor_tenant', 'engineering_contact', 'operations_contact', 'monitoring_contact']

class ServiceDeploymentImportForm(NetBoxModelImportForm):
    class Meta:
        model = models.ServiceDeployment
        fields = ['name', 'description', 'version', 'service_template', 'deployment_rfc', 'maintenance_window', 
                  'production_readiness_checklist', 'business_owner_tenant', 'business_owner_contact', 'service_owner_tenant', 
                  'service_owner_contact', 'major_incident_coordinator_contact', 'functional_area_sponsor_tenant', 
                  'functional_sub_area_sponsor_tenant', 'engineering_contact', 'operations_contact', 'monitoring_contact']

class ServiceComponentForm(NetBoxModelForm):
    class Meta:
        model = models.ServiceComponent
        fields = ['name', 'description', 'version', 'service_deployment', 'service_requirement', 'object_type', 'object_id']

class ServiceComponentImportForm(NetBoxModelImportForm):
    class Meta:
        model = models.ServiceComponent
        fields = ['name', 'description', 'version', 'service_deployment', 'service_requirement', 'object_type', 'object_id']
