from utilities.forms.fields import DynamicModelChoiceField
from django.contrib.contenttypes.models import ContentType
from .models import DynamicQuerySetModel  # Assuming a utility class

class DynamicObjectChoiceField(DynamicModelChoiceField):
    def __init__(self, object_type=None, **kwargs):
        self.object_type = object_type
        super().__init__(queryset=ContentType.objects.none(), **kwargs)

    def get_queryset(self):
        if self.object_type:
            # Use the DynamicQuerySetModel to get the queryset
            dynamic_model = DynamicQuerySetModel(self.object_type)
            return dynamic_model.get_queryset()
        return super().get_queryset()