# Generated by Django 5.0.9 on 2024-11-17 22:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netbox_servicemgmt', '0009_remove_servicedeployment_business_owner_contact_and_more'),
        ('tenancy', '0015_contactassignment_rename_content_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicecomponent',
            name='version',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='servicedeployment',
            name='version',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='servicerequirement',
            name='version',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='servicetemplate',
            name='version',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='solutionrequest',
            name='airgap_backup',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='solutionrequest',
            name='business_owner_contact',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sor_business_owners', to='tenancy.contact'),
        ),
        migrations.AlterField(
            model_name='solutionrequest',
            name='business_owner_tenant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sor_business_owners', to='tenancy.tenant'),
        ),
        migrations.AlterField(
            model_name='solutionrequest',
            name='clustered',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='solutionrequest',
            name='data_classification',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='solutionrequest',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='solutionrequest',
            name='functional_area_sponsor_tenant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sor_fa_owners', to='tenancy.tenant'),
        ),
        migrations.AlterField(
            model_name='solutionrequest',
            name='functional_sub_area_sponsor_tenant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sor_sfa_owners', to='tenancy.tenant'),
        ),
        migrations.AlterField(
            model_name='solutionrequest',
            name='multi_region',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='solutionrequest',
            name='multi_site',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='solutionrequest',
            name='offsite_backup',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='solutionrequest',
            name='offsite_replication',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='solutionrequest',
            name='rfp_status',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='solutionrequest',
            name='service_owner_contact',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sor_service_owners', to='tenancy.contact'),
        ),
        migrations.AlterField(
            model_name='solutionrequest',
            name='service_owner_tenant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sor_service_owners', to='tenancy.tenant'),
        ),
        migrations.AlterField(
            model_name='solutionrequest',
            name='slo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sor_slo', to='netbox_servicemgmt.slo'),
        ),
        migrations.AlterField(
            model_name='solutionrequest',
            name='version',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='solutiontemplate',
            name='version',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]