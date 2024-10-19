from rest_framework.viewsets import ModelViewSet
from .models import SolutionTemplate, ServiceTemplate, ServiceRequirement, SolutionDeployment, ServiceDeployment, ServiceComponent, HAModel, SLO
from .serializers import SolutionTemplateSerializer, ServiceTemplateSerializer, ServiceRequirementSerializer, SolutionDeploymentSerializer, ServiceDeploymentSerializer, ServiceComponentSerializer, HAModelSerializer, SLOSerializer

class SolutionTemplateViewSet(ModelViewSet):
    queryset = SolutionTemplate.objects.all()
    serializer_class = SolutionTemplateSerializer

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

class HAModelViewSet(ModelViewSet):
    queryset = HAModel.objects.all()
    serializer_class = HAModelSerializer

class SLOViewSet(ModelViewSet):
    queryset = SLO.objects.all()
    serializer_class = SLOSerializer
