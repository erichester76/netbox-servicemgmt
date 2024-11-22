from netbox.forms import NetBoxModelForm, NetBoxModelImportForm
from utilities.forms.fields import DynamicModelChoiceField, ContentTypeChoiceField
from . import models
from django import forms
from django.contrib.contenttypes.models import ContentType
from virtualization.models import VirtualMachine
from django.contrib.contenttypes.models import ContentType

from .models import ServiceComponent
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
                'service_owner_tenant', 'service_owner_contact', 'functional_area_sponsor_tenant', 
                'functional_sub_area_sponsor_tenant', 'rfp_status', 'rfp_ref', 'slo', 'data_classification', 'clustered', 'multi_site', 
                'multi_region', 'offsite_backup', 'airgap_backup', 'requirements']

class SolutionRequestImportForm(NetBoxModelImportForm):
    class Meta:
        model = models.SolutionRequest
        fields = ['name', 'description', 'version', 'solution_type', 'design_contact', 'business_owner_contact', 'business_owner_tenant', 
                'service_owner_tenant', 'service_owner_contact', 'functional_area_sponsor_tenant', 
                'functional_sub_area_sponsor_tenant', 'rfp_status', 'rfp_ref', 'slo', 'data_classification', 'clustered', 'multi_site', 
                'multi_region', 'offsite_backup', 'airgap_backup', 'requirements']

class SolutionTemplateForm(NetBoxModelForm):
    class Meta:
        model = models.SolutionTemplate
        fields = ['name', 'description', 'version', 'solution_request', 'solution_type', 'design_contact', 
                'slo', 'fault_tolerence', 'data_classification', 'sla_number', 'vendors'] 
        
class SolutionTemplateImportForm(NetBoxModelImportForm):
    class Meta:
        model = models.SolutionTemplate
        fields = ['name', 'description', 'version', 'solution_request', 'solution_type', 'design_contact', 
                'slo', 'fault_tolerence', 'data_classification', 'sla_number', 'vendors']  
              
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
        fields = ['name', 'description', 'version', 'solution_templates', 'design_contact', 'service_type', 'vendor', 
                  'vendor_management_number', 'vendor_management_status', 'fault_tolerence', 'service_slo']

class ServiceTemplateImportForm(NetBoxModelImportForm):
    class Meta:
        model = models.ServiceTemplate
        fields = ['name', 'description', 'version', 'solution_templates', 'design_contact', 'service_type', 'vendor', 
                  'vendor_management_number', 'vendor_management_status', 'fault_tolerence', 'service_slo']


class ServiceRequirementForm(NetBoxModelForm):
    
    class Meta:
        model = models.ServiceRequirement
        fields = ['name', 'description', 'service_template', 'requirement_owner', 'fault_tolerence', 'service_slo']


class ServiceRequirementImportForm(NetBoxModelImportForm):
    
    class Meta:
        model = models.ServiceRequirement
        fields = ['name', 'description', 'service_template', 'requirement_owner', 'service_slo']

        
class ServiceDeploymentForm(NetBoxModelForm):
    class Meta:
        model = models.ServiceDeployment
        fields = ['name', 'description', 'version', 'service_template', 'deployment_rfc', 'maintenance_window', 
                  'production_readiness_checklist', 'major_incident_coordinator_contact', 'engineering_contact', 'operations_contact', 'monitoring_contact']

class ServiceDeploymentImportForm(NetBoxModelImportForm):
    class Meta:
        model = models.ServiceDeployment
        fields = ['name', 'description', 'version', 'service_template', 'deployment_rfc', 'maintenance_window', 
                  'production_readiness_checklist', 'major_incident_coordinator_contact', 'engineering_contact', 'operations_contact', 'monitoring_contact']


class ServiceComponentForm(NetBoxModelForm):
    object_type = ContentTypeChoiceField(
        queryset=ContentType.objects.all(),
        required=True,
        label="Component Type",
    )

    object_id = DynamicModelChoiceField(
        queryset=None,  # Set dynamically via JavaScript and `widget_filter`
        required=True,
        label="Component",
    )

    class Meta:
        model = ServiceComponent
        fields = [
            "name",
            "description",
            "version",
            "service_deployment",
            "service_requirement",
            "object_type",
            "object_id",
            "tags",
        ]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Check if `object_type` is pre-populated in the form (e.g., during editing)
        object_type = self.initial.get("object_type") or self.data.get("object_type")
        if object_type:
            try:
                # Dynamically set queryset for object_id based on the selected object_type
                model_class = ContentType.objects.get(pk=object_type).model_class()
                self.fields["object_id"].queryset = model_class.objects.all()
            except ContentType.DoesNotExist:
                pass

class ServiceComponentImportForm(NetBoxModelImportForm):
    class Meta:
        model = models.ServiceComponent
        fields = ['name', 'description', 'version', 'service_deployment', 'service_requirement', 'object_type', 'object_id']
