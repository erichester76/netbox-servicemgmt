import django_filters
from netbox.filtersets import NetBoxModelFilterSet
from .models import SLA, SLO, SolutionTemplate, FaultTolerance, ServiceTemplate, ServiceRequirement, ServiceDeployment, ServiceComponent
from dcim.models import Site
from tenancy.models import Tenant, Contact
from taggit.models import Tag

# SLO FilterSet
class SLOFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = SLO
        fields = ('name', 'rpo', 'rto', 'sev1_response', 'sev2_response')

# SLA FilterSet
class SLAFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = SLA
        fields = ('name', 'description', 'slo', 'business_owner_contact', 'business_owner_tenant', 'technical_contact', 'data_classification' )
        
# SolutionTemplate FilterSet
class SolutionTemplateFilterSet(NetBoxModelFilterSet):
    design_contact = django_filters.ModelChoiceFilter(queryset=Contact.objects.all())

    class Meta:
        model = SolutionTemplate
        fields = ('name', 'design_contact', 'requirements')

# FaultTolerance FilterSet
class FaultToleranceFilterSet(NetBoxModelFilterSet):
    primary_site = django_filters.ModelChoiceFilter(queryset=Site.objects.all())
    secondary_site = django_filters.ModelChoiceFilter(queryset=Site.objects.all())
    tertiary_site = django_filters.ModelChoiceFilter(queryset=Site.objects.all())

    class Meta:
        model = FaultTolerance
        fields = ('name', 'primary_site', 'secondary_site', 'tertiary_site', 'instances_per_site')

# ServiceTemplate FilterSet
class ServiceTemplateFilterSet(NetBoxModelFilterSet):
    design_contact = django_filters.ModelChoiceFilter(queryset=Contact.objects.all())
    vendor = django_filters.ModelChoiceFilter(queryset=Tenant.objects.all())
    tags = django_filters.ModelMultipleChoiceFilter(queryset=Tag.objects.all())

    class Meta:
        model = ServiceTemplate
        fields = ('name', 'solution_template', 'design_contact', 'service_type', 'vendor', 'tags')

# ServiceRequirement FilterSet
class ServiceRequirementFilterSet(NetBoxModelFilterSet):
    primary_site = django_filters.ModelChoiceFilter(queryset=Site.objects.all())
    secondary_site = django_filters.ModelChoiceFilter(queryset=Site.objects.all())
    tertiary_site = django_filters.ModelChoiceFilter(queryset=Site.objects.all())

    class Meta:
        model = ServiceRequirement
        fields = ('name', 'service_template', 'requirement_owner', 'service_slo', 'primary_site', 'secondary_site')

# ServiceDeployment FilterSet
class ServiceDeploymentFilterSet(NetBoxModelFilterSet):
    business_owner_tenant = django_filters.ModelChoiceFilter(queryset=Tenant.objects.all())
    service_owner_tenant = django_filters.ModelChoiceFilter(queryset=Tenant.objects.all())

    class Meta:
        model = ServiceDeployment
        fields = ('name', 'service_template', 'solution_deployment', 'business_owner_tenant', 'service_owner_tenant')

# ServiceComponent FilterSet
class ServiceComponentFilterSet(NetBoxModelFilterSet):
    service_deployment = django_filters.ModelChoiceFilter(queryset=ServiceDeployment.objects.all())
    service_requirement = django_filters.ModelChoiceFilter(queryset=ServiceRequirement.objects.all())

    class Meta:
        model = ServiceComponent
        fields = ('name', 'service_deployment', 'service_requirement', 'content_object')
 """