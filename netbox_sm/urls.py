from django.urls import path
from . import views, models

urlpatterns = [
    
    path('<str:app_label>/<str:model_name>/<int:pk>/attach/', views.GenericAttachView.as_view(), name='generic_attach'),

    # Solution Template URLs
    path('solutions/', views.SolutionListView.as_view(), name='solution_list'),
    path('solutions/<int:pk>/', views.SolutionDetailView.as_view(), name='solution'),
    path('solutions/add/', views.SolutionEditView.as_view(), name='solution_add'),
    path('solutions/<int:pk>/edit/', views.SolutionEditView.as_view(), name='solution_edit'),
    path('solutions/<int:pk>/delete/', views.SolutionDeleteView.as_view(), name='solution_delete'),
    path('solutions/bulk-import/', views.SolutionBulkImportView.as_view(), name='solution_bulk_import'),
    path('solutions/<int:pk>/changelog/', views.SolutionChangeLogView.as_view(), name='solution_changelog', kwargs={'model': models.Solution}),

    # Service Deployment URLs
    path('deployments/', views.DeploymentListView.as_view(), name='deployment_list'),
    path('deployments/<int:pk>/', views.DeploymentDetailView.as_view(), name='deployment'),
    path('deployments/add/', views.DeploymentEditView.as_view(), name='deployment_add'),
    path('deployments/<int:pk>/edit/', views.DeploymentEditView.as_view(), name='deployment_edit'),
    path('deployments/<int:pk>/delete/', views.DeploymentDeleteView.as_view(), name='deployment_delete'),
    path('deployments/bulk-import/', views.DeploymentBulkImportView.as_view(), name='deployment_bulk_import'),
    path('deployments/<int:pk>/changelog/', views.DeploymentChangeLogView.as_view(), name='deployment_changelog', kwargs={'model': models.Deployment}),

    # Service Component URLs
    path('components/', views.ComponentListView.as_view(), name='component_list'),
    path('components/<int:pk>/', views.ComponentDetailView.as_view(), name='component'),
    path('components/add/', views.ComponentEditView.as_view(), name='component_add'),
    path('components/<int:pk>/edit/', views.ComponentEditView.as_view(), name='component_edit'),
    path('components/<int:pk>/delete/', views.ComponentDeleteView.as_view(), name='component_delete'),
    path('components/bulk-import/', views.ComponentBulkImportView.as_view(), name='component_bulk_import'),
    path('components/<int:pk>/changelog/', views.ComponentChangeLogView.as_view(), name='component_changelog', kwargs={'model': models.Component}),

    # High Availability (HA) Model URLs
    path('fault-tolerence/', views.FaultTolerenceListView.as_view(), name='faulttolerence_list'),
    path('fault-tolerence/<int:pk>/', views.FaultTolerenceDetailView.as_view(), name='faulttolerence'),
    path('fault-tolerence/add/', views.FaultTolerenceEditView.as_view(), name='faulttolerence_add'),
    path('fault-tolerence/<int:pk>/edit/', views.FaultTolerenceEditView.as_view(), name='faulttolerence_edit'),
    path('fault-tolerence/<int:pk>/delete/', views.FaultTolerenceDeleteView.as_view(), name='faulttolerence_delete'),
    path('fault-tolerence/bulk-import/', views.FaultTolerenceBulkImportView.as_view(), name='faulttolerence_bulk_import'),
    path('fault-tolerence/<int:pk>/changelog/', views.FaultTolerenceChangeLogView.as_view(), name='faulttolerence_changelog', kwargs={'model': models.FaultTolerence}),

    # Service Level Objective (SLO) URLs
    path('slos/', views.SLOListView.as_view(), name='slo_list'),
    path('slos/<int:pk>/', views.SLODetailView.as_view(), name='slo'),
    path('slos/add/', views.SLOEditView.as_view(), name='slo_add'),
    path('slos/<int:pk>/edit/', views.SLOEditView.as_view(), name='slo_edit'),
    path('slos/<int:pk>/delete/', views.SLODeleteView.as_view(), name='slo_delete'),
    path('slos/bulk-import/', views.SLOBulkImportView.as_view(), name='slo_bulk_import'),
    path('slos/<int:pk>/changelog/', views.SLOChangeLogView.as_view(), name='slo_changelog',  kwargs={'model': models.SLO}),

]
