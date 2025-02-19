from netbox.forms import NetBoxModelForm, NetBoxModelImportForm
from utilities.forms.fields import ContentTypeChoiceField
from . import models
from django import forms
from django.contrib.contenttypes.models import ContentType
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

class SolutionForm(NetBoxModelForm):
    class Meta:
        model = models.Solution
        fields = '__all__'
        
class SolutionImportForm(NetBoxModelImportForm):
    class Meta:
        model = models.Solution
        fields = '__all__'

class FaultTolerenceForm(NetBoxModelForm):
    class Meta:
        model = models.FaultTolerence
        fields = '__all__'

class FaultTolerenceImportForm(NetBoxModelImportForm):
    class Meta:
        model = models.FaultTolerence
        fields = '__all__'

class DeploymentForm(NetBoxModelForm):
    class Meta:
        model = models.Deployment
        fields = '__all__'

class DeploymentImportForm(NetBoxModelImportForm):
    class Meta:
        model = models.Deployment
        fields = '__all__'

class ComponentForm(NetBoxModelForm):
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
        model = models.Component
        fields = '__all__'
                
class ComponentImportForm(NetBoxModelImportForm):
    class Meta:
        model = models.Component
        fields = '__all__'
