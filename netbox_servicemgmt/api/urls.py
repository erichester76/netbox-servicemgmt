from rest_framework.routers import DefaultRouter
from .views import SolutionTemplateViewSet, ServiceTemplateViewSet, ServiceRequirementViewSet, SolutionDeploymentViewSet, ServiceDeploymentViewSet, ServiceComponentViewSet, HAModelViewSet, SLOViewSet

router = DefaultRouter()
router.register(r'solution-templates', SolutionTemplateViewSet)
router.register(r'service-templates', ServiceTemplateViewSet)
router.register(r'service-requirements', ServiceRequirementViewSet)
router.register(r'solution-deployments', SolutionDeploymentViewSet)
router.register(r'service-deployments', ServiceDeploymentViewSet)
router.register(r'service-components', ServiceComponentViewSet)
router.register(r'ha-models', HAModelViewSet)
router.register(r'slos', SLOViewSet)

urlpatterns = router.urls
