import django_filters
from netbox.filtersets import NetBoxModelFilterSet
from .models import Solution, Deployment, Component
from dcim.models import Site
from ipam.models import VLAN, Prefix
from django.contrib.contenttypes.models import ContentType
from utilities.filters import ContentTypeFilter

class SolutionFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = Solution
        fields = (
            'id', 'name', 'solution_number', 'project_id', 'data_classification',
            'production_readiness_status', 'vendor_management_status',
        )

    # Filters for choice fields (assuming they use choices or simple values)
    data_classification = django_filters.MultipleChoiceFilter(
        choices=[(v, v) for v in Solution._meta.get_field('data_classification').choices]
        if Solution._meta.get_field('data_classification').choices
        else [('public', 'Public'), ('private', 'Private'), ('confidential', 'Confidential')]
    )
    production_readiness_status = django_filters.MultipleChoiceFilter(
        choices=[(v, v) for v in Solution._meta.get_field('production_readiness_status').choices]
        if Solution._meta.get_field('production_readiness_status').choices
        else [('ready', 'Ready'), ('pending', 'Pending'), ('not_ready', 'Not Ready')]
    )
    vendor_management_status = django_filters.MultipleChoiceFilter(
        choices=[(v, v) for v in Solution._meta.get_field('vendor_management_status').choices]
        if Solution._meta.get_field('vendor_management_status').choices
        else [('active', 'Active'), ('inactive', 'Inactive')]
    )

    # Filters for name-based lookups
    name = django_filters.CharFilter(lookup_expr='icontains')
    solution_number = django_filters.CharFilter(lookup_expr='icontains')
    project_id = django_filters.CharFilter(lookup_expr='exact')

    # Filters for contact-related fields (assuming they are CharFields or ForeignKeys)
    requester = django_filters.CharFilter(lookup_expr='icontains')
    architect = django_filters.CharFilter(lookup_expr='icontains')
    business_owner_group = django_filters.CharFilter(lookup_expr='icontains')
    business_owner_contact = django_filters.CharFilter(lookup_expr='icontains')
    incident_contact = django_filters.CharFilter(lookup_expr='icontains')
    os_technical_contact_group = django_filters.CharFilter(lookup_expr='icontains')
    os_technical_contact = django_filters.CharFilter(lookup_expr='icontains')
    app_technical_contact_group = django_filters.CharFilter(lookup_expr='icontains')
    app_technical_contact = django_filters.CharFilter(lookup_expr='icontains')

class DeploymentFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = Deployment
        fields = (
            'id', 'name', 'description', 'version', 'status', 'deployment_type',
            'deployment_solution', 'deployment_vlan', 'deployment_prefix',
            'deployment_site', 'previous_version',
        )

    # Filters for choice fields
    status = django_filters.MultipleChoiceFilter(
        choices=Deployment._meta.get_field('status').choices
    )
    deployment_type = django_filters.MultipleChoiceFilter(
        choices=Deployment._meta.get_field('deployment_type').choices
    )

    # Filters for name-based lookups
    name = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')

    # Filters for ForeignKey relationships
    deployment_solution = django_filters.ModelMultipleChoiceFilter(
        queryset=Solution.objects.all(),
        field_name='deployment_solution__id',
        label='Solution'
    )
    deployment_vlan = django_filters.ModelMultipleChoiceFilter(
        queryset=VLAN.objects.all(),
        field_name='deployment_vlan__id',
        label='VLAN'
    )
    deployment_prefix = django_filters.ModelMultipleChoiceFilter(
        queryset=Prefix.objects.all(),
        field_name='deployment_prefix__id',
        label='Prefix'
    )
    deployment_site = django_filters.ModelMultipleChoiceFilter(
        queryset=Site.objects.all(),
        field_name='deployment_site__id',
        label='Site'
    )
    previous_version = django_filters.ModelMultipleChoiceFilter(
        queryset=Deployment.objects.all(),
        field_name='previous_version__id',
        label='Previous Version'
    )

class ComponentFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = Component
        fields = (
            'id', 'name', 'description', 'version', 'status', 'component_deployment',
            'component_prefix', 'component_vlan', 'component_site', 'object_type',
            'previous_version',
        )

    # Filters for choice fields
    status = django_filters.MultipleChoiceFilter(
        choices=Component._meta.get_field('status').choices
    )

    # Filters for name-based lookups
    name = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')

    # Filters for ForeignKey relationships
    component_deployment = django_filters.ModelMultipleChoiceFilter(
        queryset=Deployment.objects.all(),
        field_name='component_deployment__id',
        label='Deployment'
    )
    component_prefix = django_filters.ModelMultipleChoiceFilter(
        queryset=Prefix.objects.all(),
        field_name='component_prefix__id',
        label='Prefix'
    )
    component_vlan = django_filters.ModelMultipleChoiceFilter(
        queryset=VLAN.objects.all(),
        field_name='component_vlan__id',
        label='VLAN'
    )
    component_site = django_filters.ModelMultipleChoiceFilter(
        queryset=Site.objects.all(),
        field_name='component_site__id',
        label='Site'
    )
    previous_version = django_filters.ModelMultipleChoiceFilter(
        queryset=Component.objects.all(),
        field_name='previous_version__id',
        label='Previous Version'
    )

    # Filter for GenericForeignKey
    object_type = ContentTypeFilter(
        queryset=ContentType.objects.filter(
            app_label__in=['virtualization', 'dcim'],
            model__in=['virtualmachine', 'device']
        ),
        label='Object Type'
    )
    object_id = django_filters.NumberFilter(
        field_name='object_id',
        label='Object ID'
    )