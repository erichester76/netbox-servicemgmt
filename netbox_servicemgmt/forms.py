from netbox.forms import NetBoxModelForm, NetBoxModelImportForm
from utilities.forms.fields import DynamicModelChoiceField, ContentTypeChoiceField
from . import models
from django import forms
from django.contrib.contenttypes.models import ContentType
from virtualization.models import VirtualMachine
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
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
        
class SLOForm(NetBoxModelForm):
    class Meta:
        model = models.SLO
        fields = '__all__'

class SLOImportForm(NetBoxModelImportForm):
    class Meta:
        model = models.SLO
        fields = '__all__'

class SLAForm(NetBoxModelForm):
    class Meta:
        model = models.SLA
        virtual_machines = forms.ModelMultipleChoiceField(
            queryset=VirtualMachine.objects.all(),
            required=False
        )
        fields = '__all__'

class SLAImportForm(NetBoxModelImportForm):
    class Meta:
        model = models.SLA
        fields = '__all__'


class SolutionRequestForm(NetBoxModelForm):
    class Meta:
        model = models.SolutionRequest
        fields = '__all__'

class SolutionRequestImportForm(NetBoxModelImportForm):
    class Meta:
        model = models.SolutionRequest
        fields = '__all__'

class SolutionTemplateForm(NetBoxModelForm):
    class Meta:
        model = models.SolutionTemplate
        fields = '__all__'

        
class SolutionTemplateImportForm(NetBoxModelImportForm):
    class Meta:
        model = models.SolutionTemplate
        fields = '__all__'

class FaultTolerenceForm(NetBoxModelForm):
    class Meta:
        model = models.FaultTolerence
        fields = '__all__'

class FaultTolerenceImportForm(NetBoxModelImportForm):
    class Meta:
        model = models.FaultTolerence
        fields = '__all__'


class ServiceTemplateForm(NetBoxModelForm):
    class Meta:
        model = models.ServiceTemplate
        fields = '__all__'


class ServiceTemplateImportForm(NetBoxModelImportForm):
    class Meta:
        model = models.ServiceTemplate
        fields = '__all__'



class ServiceRequirementForm(NetBoxModelForm):
    
    class Meta:
        model = models.ServiceRequirement
        fields = '__all__'


class ServiceRequirementImportForm(NetBoxModelImportForm):
    
    class Meta:
        model = models.ServiceRequirement
        fields = '__all__'

        
class ServiceDeploymentForm(NetBoxModelForm):
    class Meta:
        model = models.ServiceDeployment
        fields = '__all__'

class ServiceDeploymentImportForm(NetBoxModelImportForm):
    class Meta:
        model = models.ServiceDeployment
        fields = '__all__'


class ServiceComponentForm(NetBoxModelForm):
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
        model = models.ServiceComponent
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
                
class ServiceComponentImportForm(NetBoxModelImportForm):
    class Meta:
        model = models.ServiceComponent
        fields = '__all__'
