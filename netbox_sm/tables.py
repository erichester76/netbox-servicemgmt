import django_tables2 as tables
from netbox.tables import NetBoxTable, ChoiceFieldColumn, columns
from tenancy.models import Tenant, Contact
from dcim.models import Site
from .models import SLO, FaultTolerence, Solution, Deployment, Component

# Service Level Objective (SLO) Table
class SLOTable(NetBoxTable):
    name = tables.Column(linkify=True)
    description = tables.Column()
    rpo = tables.Column(verbose_name='RPO (hours)')
    rto = tables.Column(verbose_name='RTO (hours)')
    sev1_response = tables.Column(verbose_name='Sev 1 Response (min)', empty_values=(None,))
    sev2_response = tables.Column(verbose_name='Sev 2 Response (min)', empty_values=(None,))
    sev3_response = tables.Column(verbose_name='Sev 3 Response (min)', empty_values=(None,))

    class Meta(NetBoxTable.Meta):
        model = SLO
        fields = ('pk', 'name', 'description', 'rpo', 'rto', 'sev1_response', 'sev2_response', 'sev3_response', 'created', 'last_updated')
        default_columns = ('name', 'description', 'rpo', 'rto')

# Fault Tolerance Table
class FaultTolerenceTable(NetBoxTable):
    name = tables.Column(linkify=True)
    description = tables.Column()
    multi_site = columns.BooleanColumn()
    multi_region = columns.BooleanColumn()
    multi_cloud = columns.BooleanColumn()
    primary_site = tables.Column(linkify=True)
    secondary_site = tables.Column(linkify=True, empty_values=(None,))
    tertiary_site = tables.Column(linkify=True, empty_values=(None,))
    gtm_required = columns.BooleanColumn()
    ltm_required = columns.BooleanColumn()
    snapshots = columns.BooleanColumn()
    storage_replication = columns.BooleanColumn()
    vm_replication = columns.BooleanColumn()
    backups = columns.BooleanColumn()
    backup_schedule = tables.Column(empty_values=(None,))
    offsite_backup = columns.BooleanColumn()
    airgap_backup = columns.BooleanColumn()

    class Meta(NetBoxTable.Meta):
        model = FaultTolerence
        fields = (
            'pk', 'name', 'description', 'multi_site', 'multi_region', 'multi_cloud', 
            'primary_site', 'secondary_site', 'tertiary_site', 'gtm_required', 'ltm_required',
            'snapshots', 'storage_replication', 'vm_replication', 'backups', 'backup_schedule',
            'offsite_backup', 'airgap_backup', 'created', 'last_updated'
        )
        default_columns = ('name', 'description', 'primary_site', 'multi_site', 'multi_region', 'multi_cloud')

# Solution Table
class SolutionTable(NetBoxTable):
    name = tables.Column(linkify=True)
    solution_number = tables.Column()
    project_id = tables.Column()
    description = tables.Column()
    solution_type = ChoiceFieldColumn()
    version = tables.Column(empty_values=(None,))
    architect = tables.Column(linkify=True, empty_values=(None,))
    requester = tables.Column(linkify=True, empty_values=(None,))
    business_owner_group = tables.Column(linkify=True, empty_values=(None,))
    business_owner_contact = tables.Column(linkify=True, empty_values=(None,))
    os_technical_contact_group = tables.Column(linkify=True, empty_values=(None,))
    os_technical_contact = tables.Column(linkify=True, empty_values=(None,))
    app_technical_contact_group = tables.Column(linkify=True, empty_values=(None,))
    app_technical_contact = tables.Column(linkify=True, empty_values=(None,))
    incident_contact = tables.Column(linkify=True, empty_values=(None,))
    data_classification = ChoiceFieldColumn()
    compliance_requirements = tables.Column(empty_values=(None,))
    fault_tolerence = tables.Column(linkify=True, empty_values=(None,))
    slos = tables.Column(linkify=True, empty_values=(None,))
    last_bcdr_test = columns.DateColumn(empty_values=(None,))
    last_risk_assessment = columns.DateColumn(empty_values=(None,))
    last_review = columns.DateColumn(empty_values=(None,))
    production_readiness_status = tables.Column(empty_values=(None,))
    vendor_management_status = tables.Column(empty_values=(None,))
    status = ChoiceFieldColumn()
    previous_version = tables.Column(linkify=True, empty_values=(None,))

    class Meta(NetBoxTable.Meta):
        model = Solution
        fields = (
            'pk', 'name', 'solution_number', 'project_id', 'description', 'solution_type', 'version',
            'architect', 'requester', 'business_owner_group', 'business_owner_contact',
            'os_technical_contact_group', 'os_technical_contact', 'app_technical_contact_group',
            'app_technical_contact', 'incident_contact', 'data_classification', 'compliance_requirements',
            'fault_tolerence', 'slos', 'last_bcdr_test', 'last_risk_assessment', 'last_review',
            'production_readiness_status', 'vendor_management_status', 'status', 'previous_version',
            'created', 'last_updated'
        )
        default_columns = ('name', 'solution_number', 'solution_type', 'version', 'status', 'description')

# Deployment Table
class DeploymentTable(NetBoxTable):
    name = tables.Column(linkify=True)
    description = tables.Column()
    version = tables.Column(empty_values=(None,))
    status = ChoiceFieldColumn()
    deployment_type = ChoiceFieldColumn()
    deployment_solution = tables.Column(linkify=True, empty_values=(None,))
    deployment_vlan = tables.Column(linkify=True, empty_values=(None,))
    deployment_prefix = tables.Column(linkify=True, empty_values=(None,))
    deployment_site = tables.Column(linkify=True, empty_values=(None,))

    previous_version = tables.Column(linkify=True, empty_values=(None,))

    class Meta(NetBoxTable.Meta):
        model = Deployment
        fields = (
            'pk', 'name', 'description', 'version', 'status', 'deployment_type',
            'deployment_solution', 'deployment_vlan', 'deployment_prefix', 'deployment_site',
            'previous_version', 'created', 'last_updated'
        )
        default_columns = ('deployment_solution', 'name', 'deployment_type', 'version', 'status')
        
# Component Table
class ComponentTable(NetBoxTable):
    name = tables.Column(linkify=True)
    description = tables.Column()
    version = tables.Column(empty_values=(None,))
    status = ChoiceFieldColumn()
    component_deployment = tables.Column(linkify=True, empty_values=(None,))
    component_vlan = tables.Column(linkify=True, empty_values=(None,))
    component_prefix = tables.Column(linkify=True, empty_values=(None,))
    component_site = tables.Column(linkify=True, empty_values=(None,))

    content_object = columns.ContentTypeColumn()
    previous_version = tables.Column(linkify=True, empty_values=(None,))

    class Meta(NetBoxTable.Meta):
        model = Component
        fields = (
            'pk', 'name', 'description', 'version', 'status', 'component_deployment',
            'component_vlan', 'component_prefix', 'component_site',
            'content_object', 'previous_version', 'created', 'last_updated'
        )
        default_columns = ('name', 'status', 'component_deployment', 'content_object')