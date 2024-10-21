from netbox.api.routers import NetBoxRouter
from django.urls import path
from .views import (
    SLOViewSet, SolutionTemplateViewSet, FaultToleranceViewSet,
    ServiceTemplateViewSet, ServiceRequirementViewSet,
    ServiceDeploymentViewSet, ServiceComponentViewSet,
    get_object_fields, get_ft_fields
)

app_name = 'netbox_servicemgmt'

router = NetBoxRouter()
router.register(r'slo', SLOViewSet)
router.register(r'solution-templates', SolutionTemplateViewSet)
router.register(r'fault-tolerances', FaultToleranceViewSet)
router.register(r'service-templates', ServiceTemplateViewSet)
router.register(r'service-requirements', ServiceRequirementViewSet)
router.register(r'service-deployments', ServiceDeploymentViewSet)
router.register(r'service-components', ServiceComponentViewSet)

# Combine router URLs with additional custom API paths
urlpatterns = router.urls + [
    path('object-fields/<int:object_type_id>/', get_object_fields, name='get_object_fields'),
    path('ft-fields/<int:ft_id>/', get_ft_fields, name='get_ft_fields'),

]
