# Generated by Django 5.0.9 on 2024-11-01 00:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netbox_servicemgmt', '0007_alter_sla_options_alter_sla_data_classification'),
        ('virtualization', '0040_convert_disk_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='sla',
            name='uuid',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='sla',
            name='virtual_machines',
            field=models.ManyToManyField(blank=True, related_name='sla', to='virtualization.virtualmachine'),
        ),
    ]