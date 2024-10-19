from django.urls import path
from . import views

urlpatterns = [
    # Solution Template URLs
    path('solution-templates/', views.SolutionTemplateListView.as_view(), name='solutiontemplate_list'),
    path('solution-templates/<int:pk>/', views.SolutionTemplateDetailView.as_view(), name='solutiontemplate_detail'),
    path('solution-templates/add/', views.SolutionTemplateEditView.as_view(), name='solutiontemplate_add'),
    path('solution-templates/<int:pk>/edit/', views.SolutionTemplateEditView.as_view(), name='solutiontemplate_edit'),
    path('solution-templates/<int:pk>/delete/', views.SolutionTemplateDeleteView.as_view(), name='solutiontemplate_delete'),
    path('solution-templates/bulk-import/', views.SolutionTemplateBulkImportView.as_view(), name='solutiontemplate_bulk_import'),
    path('solution-templates/<int:pk>/changelog/', views.SolutionTemplateChangeLogView.as_view(), name='solutiontemplate_changelog'),

    # Service Template URLs
    path('service-templates/', views.ServiceTemplateListView.as_view(), name='servicetemplate_list'),
    path('service-templates/<int:pk>/', views.ServiceTemplateDetailView.as_view(), name='servicetemplate_detail'),
    path('service-templates/add/', views.ServiceTemplateEditView.as_view(), name='servicetemplate_add'),
    path('service-templates/<int:pk>/edit/', views.ServiceTemplateEditView.as_view(), name='servicetemplate_edit'),
    path('service-templates/<int:pk>/delete/', views.ServiceTemplateDeleteView.as_view(), name='servicetemplate_delete'),
    path('service-templates/bulk-import/', views.ServiceTemplateBulkImportView.as_view(), name='servicetemplate_bulk_import'),
    path('service-templates/<int:pk>/changelog/', views.ServiceTemplateChangeLogView.as_view(), name='servicetemplate_changelog'),

    # Service Requirement URLs
    path('service-requirements/', views.ServiceRequirementListView.as_view(), name='servicerequirement_list'),
    path('service-requirements/<int:pk>/', views.ServiceRequirementDetailView.as_view(), name='servicerequirement_detail'),
    path('service-requirements/add/', views.ServiceRequirementEditView.as_view(), name='servicerequirement_add'),
    path('service-requirements/<int:pk>/edit/', views.ServiceRequirementEditView.as_view(), name='servicerequirement_edit'),
    path('service-requirements/<int:pk>/delete/', views.ServiceRequirementDeleteView.as_view(), name='servicerequirement_delete'),
    path('service-requirements/bulk-import/', views.ServiceRequirementBulkImportView.as_view(), name='servicerequirement_bulk_import'),
    path('service-requirements/<int:pk>/changelog/', views.ServiceRequirementChangeLogView.as_view(), name='servicerequirement_changelog'),

    # Solution Deployment URLs
    path('solution-deployments/', views.SolutionDeploymentListView.as_view(), name='solutiondeployment_list'),
    path('solution-deployments/<int:pk>/', views.SolutionDeploymentDetailView.as_view(), name='solutiondeployment_detail'),
    path('solution-deployments/add/', views.SolutionDeploymentEditView.as_view(), name='solutiondeployment_add'),
    path('solution-deployments/<int:pk>/edit/', views.SolutionDeploymentEditView.as_view(), name='solutiondeployment_edit'),
    path('solution-deployments/<int:pk>/delete/', views.SolutionDeploymentDeleteView.as_view(), name='solutiondeployment_delete'),
    path('solution-deployments/bulk-import/', views.SolutionDeploymentBulkImportView.as_view(), name='solutiondeployment_bulk_import'),
    path('solution-deployments/<int:pk>/changelog/', views.SolutionDeploymentChangeLogView.as_view(), name='solutiondeployment_changelog'),

    # Service Deployment URLs
    path('service-deployments/', views.ServiceDeploymentListView.as_view(), name='servicedeployment_list'),
    path('service-deployments/<int:pk>/', views.ServiceDeploymentDetailView.as_view(), name='servicedeployment_detail'),
    path('service-deployments/add/', views.ServiceDeploymentEditView.as_view(), name='servicedeployment_add'),
    path('service-deployments/<int:pk>/edit/', views.ServiceDeploymentEditView.as_view(), name='servicedeployment_edit'),
    path('service-deployments/<int:pk>/delete/', views.ServiceDeploymentDeleteView.as_view(), name='servicedeployment_delete'),
    path('service-deployments/bulk-import/', views.ServiceDeploymentBulkImportView.as_view(), name='servicedeployment_bulk_import'),
    path('service-deployments/<int:pk>/changelog/', views.ServiceDeploymentChangeLogView.as_view(), name='servicedeployment_changelog'),

    # Service Component URLs
    path('service-components/', views.ServiceComponentListView.as_view(), name='servicecomponent_list'),
    path('service-components/<int:pk>/', views.ServiceComponentDetailView.as_view(), name='servicecomponent_detail'),
    path('service-components/add/', views.ServiceComponentEditView.as_view(), name='servicecomponent_add'),
    path('service-components/<int:pk>/edit/', views.ServiceComponentEditView.as_view(), name='servicecomponent_edit'),
    path('service-components/<int:pk>/delete/', views.ServiceComponentDeleteView.as_view(), name='servicecomponent_delete'),
    path('service-components/bulk-import/', views.ServiceComponentBulkImportView.as_view(), name='servicecomponent_bulk_import'),
    path('service-components/<int:pk>/changelog/', views.ServiceComponentChangeLogView.as_view(), name='servicecomponent_changelog'),

    # High Availability (HA) Model URLs
    path('fault-tolerence/', views.FaultTolerenceListView.as_view(), name='faulttolerence_list'),
    path('fault-tolerence/<int:pk>/', views.FaultTolerenceDetailView.as_view(), name='faulttolerence_detail'),
    path('fault-tolerence/add/', views.FaultTolerenceEditView.as_view(), name='faulttolerence_add'),
    path('fault-tolerence/<int:pk>/edit/', views.FaultTolerenceEditView.as_view(), name='faulttolerence_edit'),
    path('fault-tolerence/<int:pk>/delete/', views.FaultTolerenceDeleteView.as_view(), name='faulttolerence_delete'),
    path('fault-tolerence/bulk-import/', views.FaultTolerenceBulkImportView.as_view(), name='faulttolerence_bulk_import'),
    path('fault-tolerence/<int:pk>/changelog/', views.FaultTolerenceChangeLogView.as_view(), name='faulttolerence_changelog'),

    # Service Level Objective (SLO) URLs
    path('slos/', views.SLOListView.as_view(), name='slo_list'),
    path('slos/<int:pk>/', views.SLODetailView.as_view(), name='slo_detail'),
    path('slos/add/', views.SLOEditView.as_view(), name='slo_add'),
    path('slos/<int:pk>/edit/', views.SLOEditView.as_view(), name='slo_edit'),
    path('slos/<int:pk>/delete/', views.SLODeleteView.as_view(), name='slo_delete'),
    path('slos/bulk-import/', views.SLOBulkImportView.as_view(), name='slo_bulk_import'),
    path('slos/<int:pk>/changelog/', views.SLOChangeLogView.as_view(), name='slo_changelog'),
]
