from netbox.forms import NetBoxModelForm, NetBoxModelImportForm
from .models import SLO, SolutionTemplate, FaultTolerance, ServiceTemplate, ServiceRequirement, SolutionDeployment, ServiceDeployment, ServiceComponent
from django import forms


class AttachForm(forms.Form):
    existing_object = forms.ModelChoiceField(
        queryset=None,  # The queryset will be set dynamically
        label="Select an existing object to attach"
    )

    def __init__(self, *args, **kwargs):
        current_object = kwargs.pop('current_object')
        related_model_class = kwargs.pop('related_model_class')  # Dynamically passed related model
        super().__init__(*args, **kwargs)

        # Populate the queryset dynamically based on the related model class
        self.fields['existing_object'].queryset = related_model_class.objects.exclude(pk__in=current_object.related_objects.all())

        
class SLOForm(NetBoxModelForm):
    class Meta:
        model = SLO
        fields = ['name', 'description', 'rpo', 'rto', 'sev1_response', 'sev2_response', 'sev3_response']

class SLOImportForm(NetBoxModelImportForm):
    class Meta:
        model = SLO
        fields = ['name', 'description', 'rpo', 'rto', 'sev1_response', 'sev2_response', 'sev3_response']

class SolutionTemplateForm(NetBoxModelForm):
    class Meta:
        model = SolutionTemplate
        fields = ['name', 'description', 'design_contact', 'requirements']
        
class SolutionTemplateImportForm(NetBoxModelImportForm):
    class Meta:
        model = SolutionTemplate
        fields = ['name', 'description', 'design_contact', 'requirements']
        
class FaultToleranceForm(NetBoxModelForm):
    class Meta:
        model = FaultTolerance
        fields = ['name', 'description', 'vip_required', 'offsite_replication', 'clustered', 'multi_site', 'multi_region', 'snapshots', 'offsite_backup', 'airgap_backup', 'primary_site', 'secondary_site', 'tertiary_site', 'instances_per_site', 'backup_schedule']

class FaultToleranceImportForm(NetBoxModelImportForm):
    class Meta:
        model = FaultTolerance
        fields = ['name', 'description', 'vip_required', 'offsite_replication', 'clustered', 'multi_site', 'multi_region', 'snapshots', 'offsite_backup', 'airgap_backup', 'primary_site', 'secondary_site', 'tertiary_site', 'instances_per_site', 'backup_schedule']

class ServiceTemplateForm(NetBoxModelForm):
    class Meta:
        model = ServiceTemplate
        fields = ['name', 'description', 'solution_templates', 'design_contact', 'service_type', 'vendor_management_assessment', 'vendor', 'fault_tolerence', 'service_slo']

class ServiceTemplateImportForm(NetBoxModelImportForm):
    class Meta:
        model = ServiceTemplate
        fields = ['name', 'description', 'solution_templates', 'design_contact', 'service_type', 'vendor_management_assessment', 'vendor', 'fault_tolerence', 'service_slo']


class ServiceRequirementForm(NetBoxModelForm):
    
    class Meta:
        model = ServiceRequirement
        fields = [
            'name', 'description', 'service_template', 'requirement_owner', 'service_slo',
            'primary_site', 'secondary_site', 'tertiary_site', 'instances_per_site', 'vip_required',
            'offsite_replication', 'clustered', 'multi_site', 'multi_region', 'snapshots', 'backup_schedule',
            'offsite_backup', 'airgap_backup', 'object_type'
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

        # Load the field names dynamically based on selected object_type
        object_type = self.initial.get('object_type')
        if object_type:
            model_class = object_type.model_class()
            for field, _ in self.requirement_fields:
                self.fields[field].widget = forms.Select(choices=self._get_model_field_choices(model_class))
        
        # Load default values from the SLO
        if self.instance and self.instance.service_slo:
            self._load_slo_defaults(self.instance.service_slo)

    def _get_model_field_choices(self, model_class):
        """ Returns a list of fields for the selected model class """
        fields = [(field.name, field.verbose_name) for field in model_class._meta.fields]
        return fields

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
        model = ServiceRequirement
        fields = [
            'name', 'description', 'service_template', 'requirement_owner', 'service_slo',
            'primary_site', 'secondary_site', 'tertiary_site', 'instances_per_site', 'vip_required',
            'offsite_replication', 'clustered', 'multi_site', 'multi_region', 'snapshots', 'backup_schedule',
            'offsite_backup', 'airgap_backup', 'object_type'
        ]

class SolutionDeploymentForm(NetBoxModelForm):
    class Meta:
        model = SolutionDeployment
        fields = ['name', 'description', 'solution_template', 'deployment_type', 'deployment_date']

class SolutionDeploymentImportForm(NetBoxModelImportForm):
    class Meta:
        model = SolutionDeployment
        fields = ['name', 'description', 'solution_template', 'deployment_type', 'deployment_date']

class ServiceDeploymentForm(NetBoxModelForm):
    class Meta:
        model = ServiceDeployment
        fields = ['name', 'description', 'service_template', 'solution_deployment', 'production_readiness_checklist', 'business_owner_tenant', 'business_owner_contact', 'service_owner_tenant', 'service_owner_contact', 'major_incident_coordinator_contact', 'functional_area_sponsor_tenant', 'functional_sub_area_sponsor_tenant', 'engineering_contact', 'operations_contact', 'monitoring_contact']

class ServiceDeploymentImportForm(NetBoxModelImportForm):
    class Meta:
        model = ServiceDeployment
        fields = ['name', 'description', 'service_template', 'solution_deployment', 'production_readiness_checklist', 'business_owner_tenant', 'business_owner_contact', 'service_owner_tenant', 'service_owner_contact', 'major_incident_coordinator_contact', 'functional_area_sponsor_tenant', 'functional_sub_area_sponsor_tenant', 'engineering_contact', 'operations_contact', 'monitoring_contact']

class ServiceComponentForm(NetBoxModelForm):
    class Meta:
        model = ServiceComponent
        fields = ['name', 'description', 'service_deployment', 'service_requirement', 'object_type', 'object_id']

class ServiceComponentImportForm(NetBoxModelImportForm):
    class Meta:
        model = ServiceComponent
        fields = ['name', 'description', 'service_deployment', 'service_requirement', 'object_type', 'object_id']
