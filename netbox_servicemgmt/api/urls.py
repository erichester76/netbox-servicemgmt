from rest_framework.routers import DefaultRouter
from .views import SLOViewSet, SolutionTemplateViewSet, FaultToleranceViewSet, ServiceTemplateViewSet, ServiceRequirementViewSet, SolutionDeploymentViewSet, ServiceDeploymentViewSet, ServiceComponentViewSet
from django.urls import path
from .views import get_object_fields

router = DefaultRouter()
router.register(r'slo', SLOViewSet)
router.register(r'solution-templates', SolutionTemplateViewSet)
router.register(r'fault-tolerances', FaultToleranceViewSet)
router.register(r'service-templates', ServiceTemplateViewSet)
router.register(r'service-requirements', ServiceRequirementViewSet)
router.register(r'solution-deployments', SolutionDeploymentViewSet)
router.register(r'service-deployments', ServiceDeploymentViewSet)
router.register(r'service-components', ServiceComponentViewSet)

urlpatterns = [
    router.urls,
    path('api/object-fields/<int:object_type_id>/', get_object_fields, name='get_object_fields'),
]

