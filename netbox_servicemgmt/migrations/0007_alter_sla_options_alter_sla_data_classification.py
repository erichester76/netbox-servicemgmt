# Generated by Django 5.0.9 on 2024-10-31 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netbox_servicemgmt', '0006_alter_servicerequirement_object_type_sla'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sla',
            options={'ordering': ['name']},
        ),
        migrations.AlterField(
            model_name='sla',
            name='data_classification',
            field=models.CharField(max_length=20),
        ),
    ]