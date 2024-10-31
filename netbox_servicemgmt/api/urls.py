from netbox.api.routers import NetBoxRouter
from django.urls import path
from . import views

app_name = 'netboxservicemgmt-api'

router = NetBoxRouter()
router.register(r'slos', views.SLOViewSet)
router.register(r'slas', views.SLAViewSet)
router.register(r'solution-templates', views.SolutionTemplateViewSet)
router.register(r'fault-tolerances', views.FaultToleranceViewSet)
router.register(r'service-templates', views.ServiceTemplateViewSet)
router.register(r'service-requirements', views.ServiceRequirementViewSet)
router.register(r'service-deployments', views.ServiceDeploymentViewSet)
router.register(r'service-components', views.ServiceComponentViewSet)

# Combine router URLs with additional custom API paths
urlpatterns = router.urls + [
    path('object-fields/<int:object_type_id>/', views.get_object_fields, name='get_object_fields'),
    path('ft-fields/<int:ft_id>/', views.get_ft_fields, name='get_ft_fields'),

]
