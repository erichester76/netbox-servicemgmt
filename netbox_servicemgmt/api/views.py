from rest_framework.viewsets import ModelViewSet
from ..models import SLO, SolutionTemplate, FaultTolerance, ServiceTemplate, ServiceRequirement, SolutionDeployment, ServiceDeployment, ServiceComponent
from .serializers import SLOSerializer, SolutionTemplateSerializer, FaultToleranceSerializer, ServiceTemplateSerializer, ServiceRequirementSerializer, SolutionDeploymentSerializer, ServiceDeploymentSerializer, ServiceComponentSerializer

class SLOViewSet(ModelViewSet):
    queryset = SLO.objects.all()
    serializer_class = SLOSerializer

class SolutionTemplateViewSet(ModelViewSet):
    queryset = SolutionTemplate.objects.all()
    serializer_class = SolutionTemplateSerializer

class FaultToleranceViewSet(ModelViewSet):
    queryset = FaultTolerance.objects.all()
    serializer_class = FaultToleranceSerializer

class ServiceTemplateViewSet(ModelViewSet):
    queryset = ServiceTemplate.objects.all()
    serializer_class = ServiceTemplateSerializer

class ServiceRequirementViewSet(ModelViewSet):
    queryset = ServiceRequirement.objects.all()
    serializer_class = ServiceRequirementSerializer

class SolutionDeploymentViewSet(ModelViewSet):
    queryset = SolutionDeployment.objects.all()
    serializer_class = SolutionDeploymentSerializer

class ServiceDeploymentViewSet(ModelViewSet):
    queryset = ServiceDeployment.objects.all()
    serializer_class = ServiceDeploymentSerializer

class ServiceComponentViewSet(ModelViewSet):
    queryset = ServiceComponent.objects.all()
    serializer_class = ServiceComponentSerializer
