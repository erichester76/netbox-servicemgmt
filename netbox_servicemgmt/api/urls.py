from netbox.api.routers import NetBoxRouter
from django.urls import path
from . import views

router = NetBoxRouter()
router.register(r'slos', views.SLOViewSet)
router.register(r'fault-tolerences', views.FaultTolerenceViewSet)
router.register(r'solutions', views.SolutionViewSet)
router.register(r'deployments', views.DeploymentViewSet)
router.register(r'components', views.ComponentViewSet)

# Combine router URLs with additional custom API paths
urlpatterns = router.urls + [
    path('object-fields/<int:object_type_id>/', views.get_object_fields, name='get_object_fields'),
    path('ft-fields/<int:ft_id>/', views.get_ft_fields, name='get_ft_fields'),

]
