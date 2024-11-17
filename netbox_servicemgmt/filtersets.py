import django_filters
from netbox.filtersets import NetBoxModelFilterSet
from .models import SLA, SLO, SolutionRequest, SolutionTemplate, FaultTolerance, ServiceTemplate, ServiceRequirement, ServiceDeployment, ServiceComponent
from dcim.models import Site
from tenancy.models import Tenant, Contact
from taggit.models import Tag

# SLO FilterSet
class SLOFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = SLO
        fields = ('name', 'rpo', 'rto')

# SLA FilterSet
class SLAFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = SLA
        fields = ('name', 'slo', 'business_owner_contact', 'business_owner_tenant', 'technical_contact', 'data_classification' )
        
# SolutionTemplate FilterSet
class SolutionTemplateFilterSet(NetBoxModelFilterSet):
    design_contact = django_filters.ModelChoiceFilter(queryset=Contact.objects.all())

    class Meta:
        model = SolutionTemplate
        fields = ('name', 'version', 'design_contact', 'business_owner_contact', 'business_owner_tenant', 'solution_type')

# SolutionRequest FilterSet
class SolutionRequestFilterSet(NetBoxModelFilterSet):
    #design_contact = django_filters.ModelChoiceFilter(queryset=Contact.objects.all())
    #business_owner_contact = django_filters.ModelChoiceFilter(queryset=Contact.objects.all())
    #business_owner_tenant = django_filters.ModelChoiceFilter(queryset=Tenant.objects.all())
   
    class Meta:
        model = SolutionRequest
        fields = ('name','version', 'design_contact', 'business_owner_contact', 'business_owner_tenant', 'solution_type')

# FaultTolerance FilterSet
class FaultToleranceFilterSet(NetBoxModelFilterSet):
    primary_site = django_filters.ModelChoiceFilter(queryset=Site.objects.all())
    secondary_site = django_filters.ModelChoiceFilter(queryset=Site.objects.all())
    tertiary_site = django_filters.ModelChoiceFilter(queryset=Site.objects.all())

    class Meta:
        model = FaultTolerance
        fields = ('name','vip_required', 'offsite_replication', 'clustered', 'multi_site', 'multi_region', 'snapshots', 'offsite_backup', 'airgap_backup', 'primary_site', 'secondary_site', 'tertiary_site', 'instances_per_site', 'backup_schedule')

# ServiceTemplate FilterSet
class ServiceTemplateFilterSet(NetBoxModelFilterSet):
    design_contact = django_filters.ModelChoiceFilter(queryset=Contact.objects.all())
    vendor = django_filters.ModelChoiceFilter(queryset=Tenant.objects.all())
    tags = django_filters.ModelMultipleChoiceFilter(queryset=Tag.objects.all())

    class Meta:
        model = ServiceTemplate
        fields = ('name','version', 'solution_templates', 'design_contact', 'service_type', 'vendor_management_assessment', 'vendor', 'fault_tolerence', 'service_slo')

# ServiceRequirement FilterSet
class ServiceRequirementFilterSet(NetBoxModelFilterSet):
    primary_site = django_filters.ModelChoiceFilter(queryset=Site.objects.all())
    secondary_site = django_filters.ModelChoiceFilter(queryset=Site.objects.all())
    tertiary_site = django_filters.ModelChoiceFilter(queryset=Site.objects.all())

    class Meta:
        model = ServiceRequirement
        fields = ('name', 'version', 'service_template', 'requirement_owner', 'service_slo',
            'primary_site', 'secondary_site', 'tertiary_site', 'instances_per_site', 'vip_required',
            'offsite_replication', 'clustered', 'multi_site', 'multi_region', 'snapshots', 'backup_schedule',
            'offsite_backup', 'airgap_backup'
        )
# ServiceDeployment FilterSet
class ServiceDeploymentFilterSet(NetBoxModelFilterSet):
    business_owner_tenant = django_filters.ModelChoiceFilter(queryset=Tenant.objects.all())
    service_owner_tenant = django_filters.ModelChoiceFilter(queryset=Tenant.objects.all())

    class Meta:
        model = ServiceDeployment
        fields = ('name', 'version', 'service_template', 'production_readiness_checklist', 'business_owner_tenant', 'business_owner_contact', 'service_owner_tenant', 'service_owner_contact', 'major_incident_coordinator_contact', 'functional_area_sponsor_tenant', 'functional_sub_area_sponsor_tenant', 'engineering_contact', 'operations_contact', 'monitoring_contact')

# ServiceComponent FilterSet
class ServiceComponentFilterSet(NetBoxModelFilterSet):
    service_deployment = django_filters.ModelChoiceFilter(queryset=ServiceDeployment.objects.all())
    service_requirement = django_filters.ModelChoiceFilter(queryset=ServiceRequirement.objects.all())

    class Meta:
        model = ServiceComponent
        fields = ( 'name', 'version', 'service_deployment', 'service_requirement')
