from django import forms
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm, NetBoxModelImportForm
from utilities.forms.fields import DynamicModelChoiceField, ContentTypeChoiceField
from .models import SLO, FaultTolerence, Solution, Deployment, Component, \
                   STATUS_CHOICES, SOLUTION_CHOICES, DATA_CHOICES, COMPLIANCE_STANDARDS, DEPLOYMENT_TYPES
from tenancy.models import Tenant, Contact
from dcim.models import Site
from ipam.models import Prefix, VLAN
from django.contrib.contenttypes.models import ContentType
from .fields import DynamicObjectChoiceField


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
        
# SLO Forms
class SLOForm(NetBoxModelForm):
    class Meta:
        model = SLO
        fields = ('name', 'description', 'rpo', 'rto', 'sev1_response', 'sev2_response', 'sev3_response')

class SLOImportForm(NetBoxModelImportForm):
    class Meta:
        model = SLO
        fields = '__all__'

class SolutionForm(NetBoxModelForm):
    # architect = DynamicModelChoiceField(queryset=Contact.objects.all(), required=False)
    # requester = DynamicModelChoiceField(queryset=Contact.objects.all(), required=False)
    # business_owner_group = DynamicModelChoiceField(queryset=Tenant.objects.all(), required=False)
    # business_owner_contact = DynamicModelChoiceField(queryset=Contact.objects.all(), required=False)
    # os_technical_contact_group = DynamicModelChoiceField(queryset=Tenant.objects.all(), required=False)
    # os_technical_contact = DynamicModelChoiceField(queryset=Contact.objects.all(), required=False)
    # app_technical_contact_group = DynamicModelChoiceField(queryset=Tenant.objects.all(), required=False)
    # app_technical_contact = DynamicModelChoiceField(queryset=Contact.objects.all(), required=False)
    # incident_contact = DynamicModelChoiceField(queryset=Contact.objects.all(), required=False)
    # fault_tolerence = DynamicModelChoiceField(queryset=FaultTolerence.objects.all(), required=False)
    # slos = DynamicModelChoiceField(queryset=SLO.objects.all(), required=False)
    # previous_version = DynamicModelChoiceField(queryset=Solution.objects.all(), required=False)

    class Meta:
        model = Solution
        fields = (
            'name', 'solution_number', 'project_id', 'description', 'solution_type', 'version',
            'architect', 'requester', 'business_owner_group', 'business_owner_contact',
            'os_technical_contact_group', 'os_technical_contact', 'app_technical_contact_group',
            'app_technical_contact', 'incident_contact', 'data_classification', 'compliance_requirements',
            'fault_tolerence', 'slos', 'last_bcdr_test', 'last_risk_assessment', 'last_review',
            'production_readiness_status', 'vendor_management_status', 'status', 'previous_version'
        )
        widgets = {
            'last_bcdr_test': forms.DateInput(),
            'last_risk_assessment': forms.DateInput(),
            'last_review': forms.DateInput(),
        }
        
class SolutionImportForm(NetBoxModelImportForm):
    class Meta:
        model = Solution
        fields = '__all__'

class FaultTolerenceForm(NetBoxModelForm):
    # primary_site = DynamicModelChoiceField(queryset=Site.objects.all(), required=False)
    # secondary_site = DynamicModelChoiceField(queryset=Site.objects.all(), required=False)
    # tertiary_site = DynamicModelChoiceField(queryset=Site.objects.all(), required=False)

    class Meta:
        model = FaultTolerence
        fields = (
            'name', 'description', 'multi_site', 'multi_region', 'multi_cloud', 'primary_site',
            'secondary_site', 'tertiary_site', 'gtm_required', 'ltm_required', 'snapshots',
            'storage_replication', 'vm_replication', 'backups', 'backup_schedule', 'offsite_backup', 'airgap_backup'
        )

class FaultTolerenceImportForm(NetBoxModelImportForm):
    class Meta:
        model = FaultTolerence
        fields = '__all__'

class DeploymentForm(NetBoxModelForm):
    
    # deployment_solution = DynamicModelChoiceField(queryset=Solution.objects.all(), required=False)
    # deployment_prefix = DynamicModelChoiceField(queryset=Prefix.objects.all(), required=False)
    # deployment_vlan = DynamicModelChoiceField(queryset=VLAN.objects.all(), required=False)
    # deployment_site = DynamicModelChoiceField(queryset=Site.objects.all(), required=False)
    # previous_version = DynamicModelChoiceField(queryset=Deployment.objects.all(), required=False)
    
    class Meta:
        model = Deployment
        fields = ('name', 'description', 'version', 'status', 'deployment_type', 'deployment_solution', 
                  'deployment_vlan', 'deployment_prefix', 'deployment_site',
                  'previous_version')

class DeploymentImportForm(NetBoxModelImportForm):
    class Meta:
        model = Deployment
        fields = '__all__'

class ComponentForm(NetBoxModelForm):
    # component_prefix = DynamicModelChoiceField(queryset=Prefix.objects.all(), required=False)
    # component_vlan = DynamicModelChoiceField(queryset=VLAN.objects.all(), required=False)
    # compionent_site = DynamicModelChoiceField(queryset=Site.objects.all(), required=False)
    
    object_type = ContentTypeChoiceField(
        queryset=ContentType.objects.all(),
        required=True,
        label="Object Type",
    )

    object_id = DynamicObjectChoiceField(
        required=True,
        label="Object"
    )
    
    class Meta:
        model = Component
        fields = ('name', 'description', 'version', 'status', 'component_deployment', 
                  'component_vlan', 'component_prefix', 'component_site',
                  'object_type', 'object_id', 'previous_version')                
        
class ComponentImportForm(NetBoxModelImportForm):
    class Meta:
        model = Component
        fields = '__all__'
