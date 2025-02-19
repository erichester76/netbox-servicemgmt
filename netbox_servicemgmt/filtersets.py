# from netbox.filtersets import NetBoxModelFilterSet
# from .models import SLO, Solution, FaultTolerence, Deployment, Component


# # SLO FilterSet
# class SLOFilterSet(NetBoxModelFilterSet):
#     class Meta:
#         model = SLO
#         fields = ('name', 'rpo', 'rto')

# # SolutionTemplate FilterSet
# class SolutionFilterSet(NetBoxModelFilterSet):

#     class Meta:
#         model = Solution
#         fields = ('name', 'version', 'solution_type')

# # FaultTolerence FilterSet
# class FaultTolerenceFilterSet(NetBoxModelFilterSet):

#     class Meta:
#         model = FaultTolerence
#         fields = ('name', 'primary_site', 'secondary_site', 'tertiary_site')

# # ServiceDeployment FilterSet
# class DeploymentFilterSet(NetBoxModelFilterSet):

#     class Meta:
#         model = Deployment
#         fields = ('name', 'version', 'deployment_solution' )
        
# # ServiceComponent FilterSet
# class ComponentFilterSet(NetBoxModelFilterSet):

#     class Meta:
#         model = Component
#         fields = ( 'name', 'version', 'component_deployment')
