from netbox.api.viewsets import NetBoxModelViewSet
from ..models import SLO, SolutionTemplate, FaultTolerance, ServiceTemplate, ServiceRequirement, ServiceDeployment, ServiceComponent
from .serializers import SLOSerializer, SolutionTemplateSerializer, FaultToleranceSerializer, ServiceTemplateSerializer, ServiceRequirementSerializer, ServiceDeploymentSerializer, ServiceComponentSerializer
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType

def get_ft_fields(request, slo_id):
    """API endpoint to get the details of a selected SLO."""
    ft = FaultTolerance.objects.get(id=ft_id)

    data = {
        'vip_required': ft.vip_required,
        'primary_site': ft.primary_site_id,
        'secondary_site': ft.secondary_site_id,
        'tertiary_site': ft.tertiary_site_id,
        'instances_per_site': ft.instances_per_site,
        # Add more fields as needed
    }

    return JsonResponse(data)

from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType

def get_object_fields(request, object_type_id):
    content_type = ContentType.objects.get(id=object_type_id)
    model_class = content_type.model_class()

    # Get all fields for the selected object type
    field_names = [field.name for field in model_class._meta.get_fields()]

    # Define a static list of fields to exclude from the response
    exclude_field_list = [
        'id', 
        'custom_field_data',
        'custom_fields', 
        'tags',
        'bookmarks', 
        'journal_entries', 
        'subscriptions', 
        'tagged_items', 
        'device_type',
        'device',
        'role',
        'ipaddress',
        'depends_on',
        'dependencies',
        'created',
        'last_updated',
        'object_id',
        'primary_ip4',
        'primary_ip6',
        'ipaddresses',
        'cluster_group',
        'cluster_type',
        'tenant',  
    ]

    # Exclude the fields in the static list
    filtered_fields = [field for field in field_names if field not in exclude_field_list]

    return JsonResponse({'fields': filtered_fields})


class SLOViewSet(NetBoxModelViewSet):
    queryset = SLO.objects.all()
    serializer_class = SLOSerializer

class SolutionTemplateViewSet(NetBoxModelViewSet):
    queryset = SolutionTemplate.objects.all()
    serializer_class = SolutionTemplateSerializer

class FaultToleranceViewSet(NetBoxModelViewSet):
    queryset = FaultTolerance.objects.all()
    serializer_class = FaultToleranceSerializer

class ServiceTemplateViewSet(NetBoxModelViewSet):
    queryset = ServiceTemplate.objects.all()
    serializer_class = ServiceTemplateSerializer

class ServiceRequirementViewSet(NetBoxModelViewSet):
    queryset = ServiceRequirement.objects.all()
    serializer_class = ServiceRequirementSerializer
    
class ServiceDeploymentViewSet(NetBoxModelViewSet):
    queryset = ServiceDeployment.objects.all()
    serializer_class = ServiceDeploymentSerializer

class ServiceComponentViewSet(NetBoxModelViewSet):
    queryset = ServiceComponent.objects.all()
    serializer_class = ServiceComponentSerializer
