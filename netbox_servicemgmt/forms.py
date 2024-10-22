from netbox.forms import NetBoxModelForm, NetBoxModelImportForm
from . import models
from django import forms
from django.contrib.contenttypes.models import ContentType
from dcim.models import Device

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

class SolutionRequestForm(NetBoxModelForm):
    class Meta:
        model = models.SolutionRequest
        fields = ['name', 'description', 'version', 'design_contact', 'business_owner_contact', 'business_owner_tenant', 'solution_type', 'requirements']
        
class SolutionRequestImportForm(NetBoxModelImportForm):
    class Meta:
        model = models.SolutionRequest
        fields = ['name', 'description', 'version', 'design_contact', 'business_owner_contact', 'business_owner_tenant', 'solution_type', 'requirements']


class SolutionTemplateForm(NetBoxModelForm):
    class Meta:
        model = models.SolutionTemplate
        fields = ['name', 'description', 'version', 'design_contact', 'business_owner_contact', 'business_owner_tenant', 'solution_type', 'requirements']
        
class SolutionTemplateImportForm(NetBoxModelImportForm):
    class Meta:
        model = models.SolutionTemplate
        fields = ['name', 'description', 'version', 'design_contact', 'business_owner_contact', 'business_owner_tenant', 'solution_type', 'requirements']
        
class FaultToleranceForm(NetBoxModelForm):
    class Meta:
        model = models.FaultTolerance
        fields = ['name', 'description', 'vip_required', 'offsite_replication', 'clustered', 'multi_site', 'multi_region', 'snapshots', 'offsite_backup', 'airgap_backup', 'primary_site', 'secondary_site', 'tertiary_site', 'instances_per_site', 'backup_schedule']

class FaultToleranceImportForm(NetBoxModelImportForm):
    class Meta:
        model = models.FaultTolerance
        fields = ['name', 'description', 'vip_required', 'offsite_replication', 'clustered', 'multi_site', 'multi_region', 'snapshots', 'offsite_backup', 'airgap_backup', 'primary_site', 'secondary_site', 'tertiary_site', 'instances_per_site', 'backup_schedule']

class ServiceTemplateForm(NetBoxModelForm):
    class Meta:
        model = models.ServiceTemplate
        fields = ['name', 'description', 'version', 'solution_templates', 'design_contact', 'service_type', 'vendor_management_assessment', 'vendor', 'fault_tolerence', 'service_slo']

class ServiceTemplateImportForm(NetBoxModelImportForm):
    class Meta:
        model = models.ServiceTemplate
        fields = ['name', 'description', 'version', 'solution_templates', 'design_contact', 'service_type', 'vendor_management_assessment', 'vendor', 'fault_tolerence', 'service_slo']


class ServiceRequirementForm(NetBoxModelForm):
    
    class Meta:
        model = models.ServiceRequirement
        fields = [
            'name', 'description', 'service_template', 'requirement_owner', 'service_slo',
            'primary_site', 'secondary_site', 'tertiary_site', 'instances_per_site', 'vip_required',
            'offsite_replication', 'clustered', 'multi_site', 'multi_region', 'snapshots', 'backup_schedule',
            'offsite_backup', 'airgap_backup', 'object_type',
        ]

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Default to 'Device' ContentType if no object_type is set
        object_type_id = self.initial.get('object_type') or self.data.get('object_type')

        # If no object_type is passed (new object), default to 'Device' object type
        if not object_type_id:
            device_content_type = ContentType.objects.get_for_model(Device)
            object_type_id = device_content_type.id
            self.initial['object_type'] = object_type_id

        # Load the field names dynamically based on the selected object_type
        try:
            object_type = ContentType.objects.get(pk=object_type_id)
            model_class = object_type.model_class()

            # Update widgets for each requirement field with the field choices from the model
            for field, _ in self.requirement_fields:
                if field in self.fields:
                    self.fields[field].widget = forms.Select(choices=self._get_model_field_choices(model_class))
        except ContentType.DoesNotExist:
            pass  # Handle the case where the ContentType doesn't exist


    def _get_model_field_choices(self, model_class):
        """Return the field choices for the given model class."""
        fields = model_class._meta.get_fields()

        # Define the list of fields to exclude
        exclude_field_list = [
            'id', 
            'created', 
            'tenant', 
            'local_context_data', 
            'description', 
            'last_updated', 
            'tags', 
            'comments', 
            'name', 
            'role',
            'serial_number'
            'cluster',
            'site',
            'custom_fields', 
            'custom_field_data',
            'status',
            'tags',
            'config_template',
            'device',
        ]

        # Return choices excluding the fields in the exclude list and reverse relations
        return [
            (field.name, field.verbose_name)
            for field in fields
            if field.concrete and field.name not in exclude_field_list and hasattr(field, 'verbose_name')
        ]
        
    def _load_slo_defaults(self, slo):
        """ Dynamically load default SLO fields if SLO is provided """
        for field in slo._meta.get_fields():
            # Skip many-to-many and reverse relations
            if field.is_relation and (field.many_to_many or field.auto_created):
                continue
            
            # Check if the form has a corresponding field
            form_field_name = field.name
            if form_field_name in self.fields:
                # Set the initial value for the form field based on the SLO field value
                self.fields[form_field_name].initial = getattr(slo, form_field_name)

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
        fields = ['name', 'description', 'version', 'service_template', 'deployment_rfc', 'maintenance_window', 'production_readiness_checklist', 'business_owner_tenant', 'business_owner_contact', 'service_owner_tenant', 'service_owner_contact', 'major_incident_coordinator_contact', 'functional_area_sponsor_tenant', 'functional_sub_area_sponsor_tenant', 'engineering_contact', 'operations_contact', 'monitoring_contact']

class ServiceDeploymentImportForm(NetBoxModelImportForm):
    class Meta:
        model = models.ServiceDeployment
        fields = ['name', 'description', 'version', 'service_template', 'deployment_rfc', 'maintenance_window', 'production_readiness_checklist', 'business_owner_tenant', 'business_owner_contact', 'service_owner_tenant', 'service_owner_contact', 'major_incident_coordinator_contact', 'functional_area_sponsor_tenant', 'functional_sub_area_sponsor_tenant', 'engineering_contact', 'operations_contact', 'monitoring_contact']

class ServiceComponentForm(NetBoxModelForm):
    class Meta:
        model = models.ServiceComponent
        fields = ['name', 'description', 'version', 'service_deployment', 'service_requirement', 'object_type', 'object_id']

class ServiceComponentImportForm(NetBoxModelImportForm):
    class Meta:
        model = models.ServiceComponent
        fields = ['name', 'description', 'version', 'service_deployment', 'service_requirement', 'object_type', 'object_id']
