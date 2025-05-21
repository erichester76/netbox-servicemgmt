from netbox.search import SearchIndex, registry
from .models import Solution, Deployment, Component

class SolutionIndex(SearchIndex):
    model = Solution
    fields = (
        ('name', 'A'),
        ('solution_number', 'A'),
        ('project_id', 'A'),
        ('data_classification', 'B'),
        ('production_readiness_status', 'B'),
        ('vendor_management_status', 'B'),
        ('requester', 'C'),
        ('architect', 'C'),
        ('business_owner_group', 'C'),
        ('business_owner_contact', 'C'),
        ('incident_contact', 'C'),
        ('os_technical_contact_group', 'C'),
        ('os_technical_contact', 'C'),
        ('app_technical_contact_group', 'C'),
        ('app_technical_contact', 'C'),
    )

class DeploymentIndex(SearchIndex):
    model = Deployment
    fields = (
        ('name', 'A'),
        ('description', 'B'),
        ('status', 'B'),
        ('deployment_type', 'B'),
    )

class ComponentIndex(SearchIndex):
    model = Component
    fields = (
        ('name', 'A'),
        ('description', 'B'),
        ('status', 'B'),
    )

# Register the indices
registry['search'].register(SolutionIndex)
registry['search'].register(DeploymentIndex)
registry['search'].register(ComponentIndex)