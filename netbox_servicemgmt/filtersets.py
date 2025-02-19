from netbox.filtersets import NetBoxModelFilterSet
from .models import SLO, Solution, FaultTolerence, Deployment, Component


# SLO FilterSet
class SLOFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = SLO
        fields = ('name', 'rpo', 'rto')

# SolutionTemplate FilterSet
class SolutionFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = Solution
        fields = ('name', 'version', 'solution_type')

# FaultTolerence FilterSet
class FaultTolerenceFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = FaultTolerence
        fields = ('name', 'vip_required', 'offsite_replication', 'clustered', 'multi_site', 'multi_region', 'snapshots', 'offsite_backup', 'airgap_backup', 'primary_site', 'secondary_site', 'tertiary_site', 'instances_per_site', 'backup_schedule')

# ServiceDeployment FilterSet
class ServiceDeploymentFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = Deployment
        fields = ('name', 'version', 'solution' )
        
# ServiceComponent FilterSet
class ServiceComponentFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = Component
        fields = ( 'name', 'version', )
