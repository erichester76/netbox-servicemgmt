from rest_framework.routers import DefaultRouter
from .views import SLOViewSet, SolutionTemplateViewSet, FaultTolerenceViewSet, ServiceTemplateViewSet, ServiceRequirementViewSet, SolutionDeploymentViewSet, ServiceDeploymentViewSet, ServiceComponentViewSet

router = DefaultRouter()
router.register(r'slo', SLOViewSet)
router.register(r'solution-templates', SolutionTemplateViewSet)
router.register(r'fault-tolerances', FaultTolerenceViewSet)
router.register(r'service-templates', ServiceTemplateViewSet)
router.register(r'service-requirements', ServiceRequirementViewSet)
router.register(r'solution-deployments', SolutionDeploymentViewSet)
router.register(r'service-deployments', ServiceDeploymentViewSet)
router.register(r'service-components', ServiceComponentViewSet)

urlpatterns = router.urls
