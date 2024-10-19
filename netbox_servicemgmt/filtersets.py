import django_filters
from .models import SolutionTemplate, ServiceTemplate, ServiceRequirement, SolutionDeployment, ServiceDeployment, ServiceComponent, HAModel, SLO
from netbox.filtersets import NetBoxModelFilterSet
from tenancy.models import Tenant
from dcim.models import Site


# SolutionTemplate FilterSet
class SolutionTemplateFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = SolutionTemplate
        fields = ['name', 'architect_contact', 'budget']


# ServiceTemplate FilterSet
class ServiceTemplateFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = ServiceTemplate
        fields = ['name', 'responsible_design', 'responsible_deployment', 'responsible_operations', 'responsible_monitoring']


# ServiceRequirement FilterSet
class ServiceRequirementFilterSet(NetBoxModelFilterSet):
    object_type = django_filters.ModelChoiceFilter(queryset=Site.objects.all())  # Example for filtering by object type

    class Meta:
        model = ServiceRequirement
        fields = ['service_template', 'requirement1', 'requirement2', 'requirement3', 'requirement20']


# SolutionDeployment FilterSet
class SolutionDeploymentFilterSet(NetBoxModelFilterSet):
    tenant = django_filters.ModelChoiceFilter(queryset=Tenant.objects.all())

    class Meta:
        model = SolutionDeployment
        fields = ['solution_template', 'tenant', 'deployment_date']


# ServiceDeployment FilterSet
class ServiceDeploymentFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = ServiceDeployment
        fields = ['service_template', 'solution_deployment']


# ServiceComponent FilterSet
class ServiceComponentFilterSet(NetBoxModelFilterSet):
    object_type = django_filters.ModelChoiceFilter(queryset=Site.objects.all())  # Example for filtering by object type

    class Meta:
        model = ServiceComponent
        fields = ['service_deployment', 'object_type']


# HAModel FilterSet
class HAModelFilterSet(NetBoxModelFilterSet):
    primary_site = django_filters.ModelChoiceFilter(queryset=Site.objects.all())
    secondary_site = django_filters.ModelChoiceFilter(queryset=Site.objects.all())
    tertiary_site = django_filters.ModelChoiceFilter(queryset=Site.objects.all())

    class Meta:
        model = HAModel
        fields = ['service_template', 'primary_site', 'secondary_site', 'tertiary_site', 'replication', 'cluster', 'multi_site']


# SLO FilterSet
class SLOFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = SLO
        fields = ['service_template', 'rpo', 'rto', 'sev1_response', 'sev2_response', 'replicas_per_site']
