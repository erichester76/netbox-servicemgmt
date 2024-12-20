# Generated by Django 5.0.9 on 2024-12-05 00:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dcim', '0191_module_bay_rebuild'),
        ('extras', '0121_customfield_related_object_filter'),
        ('netbox_servicemgmt', '0010_alter_servicecomponent_version_and_more'),
        ('tenancy', '0015_contactassignment_rename_content_type'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='FaultTolerance',
            new_name='FaultTolerence',
        ),
        migrations.RemoveField(
            model_name='servicerequirement',
            name='object_type',
        ),
        migrations.AlterField(
            model_name='servicecomponent',
            name='service_deployment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='servcom_servdeps', to='netbox_servicemgmt.servicedeployment'),
        ),
        migrations.AlterField(
            model_name='servicecomponent',
            name='service_requirement',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='servcom_servreqs', to='netbox_servicemgmt.servicerequirement'),
        ),
        migrations.AlterField(
            model_name='servicedeployment',
            name='engineering_contact',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='servdep_engineers', to='tenancy.contact'),
        ),
        migrations.AlterField(
            model_name='servicedeployment',
            name='major_incident_coordinator_contact',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='servdep_mi_owners', to='tenancy.contact'),
        ),
        migrations.AlterField(
            model_name='servicedeployment',
            name='monitoring_contact',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='servdep_monitorors', to='tenancy.contact'),
        ),
        migrations.AlterField(
            model_name='servicedeployment',
            name='operations_contact',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='servdep_operators', to='tenancy.contact'),
        ),
        migrations.AlterField(
            model_name='servicedeployment',
            name='service_template',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='servdep_servtems', to='netbox_servicemgmt.servicetemplate'),
        ),
        migrations.AlterField(
            model_name='servicerequirement',
            name='fault_tolerence',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='servreq_fts', to='netbox_servicemgmt.faulttolerence'),
        ),
        migrations.AlterField(
            model_name='servicerequirement',
            name='requirement_owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='servreq_designers', to='tenancy.contact'),
        ),
        migrations.AlterField(
            model_name='servicerequirement',
            name='service_slo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='servreq_slos', to='netbox_servicemgmt.slo'),
        ),
        migrations.AlterField(
            model_name='servicerequirement',
            name='service_template',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='servreq_servtems', to='netbox_servicemgmt.servicetemplate'),
        ),
        migrations.AlterField(
            model_name='servicetemplate',
            name='fault_tolerence',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='servtem_fts', to='netbox_servicemgmt.faulttolerence'),
        ),
        migrations.AlterField(
            model_name='servicetemplate',
            name='service_slo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='servtem_slos', to='netbox_servicemgmt.slo'),
        ),
        migrations.AlterField(
            model_name='servicetemplate',
            name='solution_templates',
            field=models.ManyToManyField(related_name='servtem_soltems', to='netbox_servicemgmt.solutiontemplate'),
        ),
        migrations.AlterField(
            model_name='servicetemplate',
            name='vendor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='servtem_vendors', to='dcim.manufacturer'),
        ),
        migrations.AlterField(
            model_name='sla',
            name='slo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sla_slos', to='netbox_servicemgmt.slo'),
        ),
        migrations.AlterField(
            model_name='solutionrequest',
            name='business_owner_contact',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='solreq_business_owners', to='tenancy.contact'),
        ),
        migrations.AlterField(
            model_name='solutionrequest',
            name='business_owner_tenant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='solreq_business_owners', to='tenancy.tenant'),
        ),
        migrations.AlterField(
            model_name='solutionrequest',
            name='design_contact',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='solreq_designers', to='tenancy.contact'),
        ),
        migrations.AlterField(
            model_name='solutionrequest',
            name='functional_area_sponsor_tenant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='solreq_fa_owners', to='tenancy.tenant'),
        ),
        migrations.AlterField(
            model_name='solutionrequest',
            name='functional_sub_area_sponsor_tenant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='solreq_sfa_owners', to='tenancy.tenant'),
        ),
        migrations.AlterField(
            model_name='solutionrequest',
            name='service_owner_contact',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='solrea_service_owners', to='tenancy.contact'),
        ),
        migrations.AlterField(
            model_name='solutionrequest',
            name='service_owner_tenant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='solreq_service_owners', to='tenancy.tenant'),
        ),
        migrations.AlterField(
            model_name='solutionrequest',
            name='slo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='solreq_slso', to='netbox_servicemgmt.slo'),
        ),
        migrations.AlterField(
            model_name='solutiontemplate',
            name='design_contact',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='designer_soltems', to='tenancy.contact'),
        ),
        migrations.AlterField(
            model_name='solutiontemplate',
            name='fault_tolerence',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ft_soltems', to='netbox_servicemgmt.faulttolerence'),
        ),
        migrations.AlterField(
            model_name='solutiontemplate',
            name='slo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='slo_soltems', to='netbox_servicemgmt.slo'),
        ),
        migrations.AlterField(
            model_name='solutiontemplate',
            name='solution_request',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='solreq_soltems', to='netbox_servicemgmt.solutionrequest'),
        ),
        migrations.AlterField(
            model_name='solutiontemplate',
            name='vendors',
            field=models.ManyToManyField(blank=True, null=True, related_name='vendors_soltems', to='dcim.manufacturer'),
        ),
    ]