import django_tables2 as tables
from netbox.tables import NetBoxTable
from .models import (
    SLO, FaultTolerence, Solution, 
    Deployment, Component
)

class SLOTable(NetBoxTable):
    name = tables.Column(linkify=True)
    
    class Meta(NetBoxTable.Meta):
        model = SLO
        fields = ('pk', 'name', 'description', 'rpo', 'rto', 'sev1_response', 'sev2_response', 'sev3_response', 'status', 'last_modified', 'created')
        default_columns = ('name', 'rpo', 'rto', 'status')

class FaultTolerenceTable(NetBoxTable):
    name = tables.Column(linkify=True)
    primary_site = tables.Column(linkify=True)
    secondary_site = tables.Column(linkify=True)
    tertiary_site = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = FaultTolerence
        fields = "__all__"
        default_columns = ('name', 'primary_site', 'vip_required', 'clustered', 'status')

class SolutionTable(NetBoxTable):
    name = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = Solution
        fields = "__all__"
        default_columns = ('name', 'version', 'solution_type', 'status')

class DeploymentTable(NetBoxTable):
    name = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = Deployment
        fields = "__all__"
        default_columns = ('name', 'version', 'solution', 'status')

class ComponentTable(NetBoxTable):
    name = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = Component
        fields = "__all__"
        default_columns = ('name', 'version', 'status')
