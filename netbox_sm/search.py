from netbox.search import SearchIndex, register_search
from .models import Solution, Deployment, Component

@register_search
class SolutionIndex(SearchIndex):
    model = Solution
    fields = (
        ('name', 100),
        ('solution_number', 100),
        ('project_id', 100),
        ('data_classification', 50),
        ('production_readiness_status', 50),
        ('vendor_management_status', 50),
        ('requester', 50),
        ('architect', 50),
        ('business_owner_group', 50),
        ('business_owner_contact', 50),
        ('incident_contact', 50),
        ('os_technical_contact_group', 50),
        ('os_technical_contact', 50),
        ('app_technical_contact_group', 50),
        ('app_technical_contact', 50),
    )

@register_search
class DeploymentIndex(SearchIndex):
    model = Deployment
    fields = (
        ('name', 100),
        ('description', 50),
        ('status', 50),
        ('deployment_type', 50),
    )

@register_search
class ComponentIndex(SearchIndex):
    model = Component
    fields = (
        ('name', 100),
        ('description', 50),
        ('status', 50),
    )