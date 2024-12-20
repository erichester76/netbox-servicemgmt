from django.urls import path
from . import views, models

urlpatterns = [
    
    path('<str:app_label>/<str:model_name>/<int:pk>/attach/', views.GenericAttachView.as_view(), name='generic_attach'),

    # Solution Template URLs
    path('solution-requests/', views.SolutionRequestListView.as_view(), name='solutionrequest_list'),
    path('solution-requests/<int:pk>/', views.SolutionRequestDetailView.as_view(), name='solutionrequest'),
    path('solution-requests/add/', views.SolutionRequestEditView.as_view(), name='solutionrequest_add'),
    path('solution-requests/<int:pk>/edit/', views.SolutionRequestEditView.as_view(), name='solutionrequest_edit'),
    path('solution-requests/<int:pk>/delete/', views.SolutionRequestDeleteView.as_view(), name='solutionrequest_delete'),
    path('solution-requests/bulk-import/', views.SolutionRequestBulkImportView.as_view(), name='solutionrequest_bulk_import'),
    path('solution-requests/<int:pk>/changelog/', views.SolutionRequestChangeLogView.as_view(), name='solutionrequest_changelog', kwargs={'model': models.SolutionRequest}),
   
    # Solution Template URLs
    path('solution-templates/', views.SolutionTemplateListView.as_view(), name='solutiontemplate_list'),
    path('solution-templates/<int:pk>/', views.SolutionTemplateDetailView.as_view(), name='solutiontemplate'),
    path('solution-templates/add/', views.SolutionTemplateEditView.as_view(), name='solutiontemplate_add'),
    path('solution-templates/<int:pk>/edit/', views.SolutionTemplateEditView.as_view(), name='solutiontemplate_edit'),
    path('solution-templates/<int:pk>/delete/', views.SolutionTemplateDeleteView.as_view(), name='solutiontemplate_delete'),
    path('solution-templates/bulk-import/', views.SolutionTemplateBulkImportView.as_view(), name='solutiontemplate_bulk_import'),
    path('solution-templates/<int:pk>/changelog/', views.SolutionTemplateChangeLogView.as_view(), name='solutiontemplate_changelog', kwargs={'model': models.SolutionTemplate}),
    path('solution-templates/<int:pk>/diagram/', views.SolutionTemplateDiagramView.as_view(), name='solutiontemplate_diagram'),

    # Service Template URLs
    path('service-templates/', views.ServiceTemplateListView.as_view(), name='servicetemplate_list'),
    path('service-templates/<int:pk>/', views.ServiceTemplateDetailView.as_view(), name='servicetemplate'),
    path('service-templates/add/', views.ServiceTemplateEditView.as_view(), name='servicetemplate_add'),
    path('service-templates/<int:pk>/edit/', views.ServiceTemplateEditView.as_view(), name='servicetemplate_edit'),
    path('service-templates/<int:pk>/delete/', views.ServiceTemplateDeleteView.as_view(), name='servicetemplate_delete'),
    path('service-templates/bulk-import/', views.ServiceTemplateBulkImportView.as_view(), name='servicetemplate_bulk_import'),
    path('service-templates/<int:pk>/changelog/', views.ServiceTemplateChangeLogView.as_view(), name='servicetemplate_changelog', kwargs={'model': models.ServiceTemplate}),
    path('service-templates/<int:pk>/diagram/', views.ServiceTemplateDiagramView.as_view(), name='servicetemplate_diagram'),

    # Service Requirement URLs
    path('service-requirements/', views.ServiceRequirementListView.as_view(), name='servicerequirement_list'),
    path('service-requirements/<int:pk>/', views.ServiceRequirementDetailView.as_view(), name='servicerequirement'),
    path('service-requirements/add/', views.ServiceRequirementEditView.as_view(), name='servicerequirement_add'),
    path('service-requirements/<int:pk>/edit/', views.ServiceRequirementEditView.as_view(), name='servicerequirement_edit'),
    path('service-requirements/<int:pk>/delete/', views.ServiceRequirementDeleteView.as_view(), name='servicerequirement_delete'),
    path('service-requirements/bulk-import/', views.ServiceRequirementBulkImportView.as_view(), name='servicerequirement_bulk_import'),
    path('service-requirements/<int:pk>/changelog/', views.ServiceRequirementChangeLogView.as_view(), name='servicerequirement_changelog', kwargs={'model': models.ServiceRequirement}),

    # Service Deployment URLs
    path('service-deployments/', views.ServiceDeploymentListView.as_view(), name='servicedeployment_list'),
    path('service-deployments/<int:pk>/', views.ServiceDeploymentDetailView.as_view(), name='servicedeployment'),
    path('service-deployments/add/', views.ServiceDeploymentEditView.as_view(), name='servicedeployment_add'),
    path('service-deployments/<int:pk>/edit/', views.ServiceDeploymentEditView.as_view(), name='servicedeployment_edit'),
    path('service-deployments/<int:pk>/delete/', views.ServiceDeploymentDeleteView.as_view(), name='servicedeployment_delete'),
    path('service-deployments/bulk-import/', views.ServiceDeploymentBulkImportView.as_view(), name='servicedeployment_bulk_import'),
    path('service-deployments/<int:pk>/changelog/', views.ServiceDeploymentChangeLogView.as_view(), name='servicedeployment_changelog', kwargs={'model': models.ServiceDeployment}),
    path('service-deployments/<int:pk>/diagram/', views.ServiceDeploymentDiagramView.as_view(), name='servicedeployment_diagram'),

    # Service Component URLs
    path('service-components/', views.ServiceComponentListView.as_view(), name='servicecomponent_list'),
    path('service-components/<int:pk>/', views.ServiceComponentDetailView.as_view(), name='servicecomponent'),
    path('service-components/add/', views.ServiceComponentEditView.as_view(), name='servicecomponent_add'),
    path('service-components/<int:pk>/edit/', views.ServiceComponentEditView.as_view(), name='servicecomponent_edit'),
    path('service-components/<int:pk>/delete/', views.ServiceComponentDeleteView.as_view(), name='servicecomponent_delete'),
    path('service-components/bulk-import/', views.ServiceComponentBulkImportView.as_view(), name='servicecomponent_bulk_import'),
    path('service-components/<int:pk>/changelog/', views.ServiceComponentChangeLogView.as_view(), name='servicecomponent_changelog', kwargs={'model': models.ServiceComponent}),

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

   # Service Level Agreements (SLA) URLs
    path('slas/', views.SLAListView.as_view(), name='sla_list'),
    path('slas/<int:pk>/', views.SLADetailView.as_view(), name='sla'),
    path('slas/add/', views.SLAEditView.as_view(), name='sla_add'),
    path('slas/<int:pk>/edit/', views.SLAEditView.as_view(), name='sla_edit'),
    path('slas/<int:pk>/delete/', views.SLADeleteView.as_view(), name='sla_delete'),
    path('slas/bulk-import/', views.SLABulkImportView.as_view(), name='sla_bulk_import'),
    path('slas/<int:pk>/changelog/', views.SLAChangeLogView.as_view(), name='sla_changelog',  kwargs={'model': models.SLA}),


]
