from netbox.filtersets import NetBoxModelFilterSet
from .models import SLA, SLO, SolutionRequest, SolutionTemplate, FaultTolerance, ServiceTemplate, ServiceRequirement, ServiceDeployment, ServiceComponent


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

    class Meta:
        model = SolutionTemplate
        fields = ('name', 'version', 'design_contact', 'solution_type')

# SolutionRequest FilterSet
class SolutionRequestFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = SolutionRequest
        fields = ('name', 'version', 'design_contact', 'business_owner_contact', 'business_owner_tenant', 'solution_type')

# FaultTolerance FilterSet
class FaultToleranceFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = FaultTolerance
        fields = ('name','vip_required', 'offsite_replication', 'clustered', 'multi_site', 'multi_region', 'snapshots', 'offsite_backup', 'airgap_backup', 'primary_site', 'secondary_site', 'tertiary_site', 'instances_per_site', 'backup_schedule')

# ServiceTemplate FilterSet
class ServiceTemplateFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = ServiceTemplate
        fields = ('name','version', 'solution_templates', 'design_contact', 'service_type')

# ServiceRequirement FilterSet
class ServiceRequirementFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = ServiceRequirement
        fields = ('name', 'version', 'service_template')
        
# ServiceDeployment FilterSet
class ServiceDeploymentFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = ServiceDeployment
        fields = ('name', 'version', 'service_template')
        
# ServiceComponent FilterSet
class ServiceComponentFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = ServiceComponent
        fields = ( 'name', 'version', 'service_deployment', 'service_requirement')
