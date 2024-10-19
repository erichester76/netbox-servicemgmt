from netbox.api.viewsets import NetBoxModelViewSet
from ..models import SLO, SolutionTemplate, FaultTolerance, ServiceTemplate, ServiceRequirement, SolutionDeployment, ServiceDeployment, ServiceComponent
from .serializers import SLOSerializer, SolutionTemplateSerializer, FaultToleranceSerializer, ServiceTemplateSerializer, ServiceRequirementSerializer, SolutionDeploymentSerializer, ServiceDeploymentSerializer, ServiceComponentSerializer
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType

def get_slo_fields(request, slo_id):
    """API endpoint to get the details of a selected SLO."""
    slo = SLO.objects.get(id=slo_id)

    data = {
        'vip_required': slo.vip_required,
        'primary_site': slo.primary_site_id,
        'secondary_site': slo.secondary_site_id,
        'tertiary_site': slo.tertiary_site_id,
        'instances_per_site': slo.instances_per_site,
        # Add more fields as needed
    }

    return JsonResponse(data)

def get_object_fields(request, object_type_id):
    """API endpoint to get fields for a given object type."""
    content_type = ContentType.objects.get(id=object_type_id)
    model_class = content_type.model_class()

    fields = [{'name': field.name, 'verbose_name': field.verbose_name} for field in model_class._meta.fields]
    
    return JsonResponse({'fields': fields})

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

class SolutionDeploymentViewSet(NetBoxModelViewSet):
    queryset = SolutionDeployment.objects.all()
    serializer_class = SolutionDeploymentSerializer

class ServiceDeploymentViewSet(NetBoxModelViewSet):
    queryset = ServiceDeployment.objects.all()
    serializer_class = ServiceDeploymentSerializer

class ServiceComponentViewSet(NetBoxModelViewSet):
    queryset = ServiceComponent.objects.all()
    serializer_class = ServiceComponentSerializer
