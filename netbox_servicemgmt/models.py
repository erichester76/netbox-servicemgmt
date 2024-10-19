from django.db import models
from netbox.models import NetBoxModel
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from tenancy.models import Tenant
from users.models import User
from dcim.models import Site
from taggit.managers import TaggableManager

# Solution Template Model
class SolutionTemplate(NetBoxModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    architect_contact = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # Refers to NetBox user/contact
    problem_statement = models.TextField()
    business_requirements = models.TextField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


# Service Template Model
class ServiceTemplate(NetBoxModel):
    name = models.CharField(max_length=255)
    solution_template = models.ForeignKey(SolutionTemplate, on_delete=models.CASCADE, related_name='service_templates')
    responsible_design = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='responsible_design')  # NetBox User
    responsible_deployment = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='responsible_deployment')
    responsible_operations = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='responsible_operations')
    responsible_monitoring = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='responsible_monitoring')

    tags = TaggableManager(related_name='netbox_servicemgmt_servicetemplates')


    def __str__(self):
        return self.name


# Service Requirement Model
class ServiceRequirement(NetBoxModel):
    service_template = models.ForeignKey(ServiceTemplate, on_delete=models.CASCADE, related_name='service_requirements')

    # Enumerated requirement fields
    requirement1 = models.CharField(max_length=255, null=True, blank=True)
    requirement2 = models.CharField(max_length=255, null=True, blank=True)
    requirement3 = models.CharField(max_length=255, null=True, blank=True)
    # ... Continue this pattern until requirement20
    requirement20 = models.CharField(max_length=255, null=True, blank=True)

    # Object Type field to link to any NetBox object type
    object_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to={
        'model__in': ('device', 'virtualmachine', 'circuit', 'interface')  # List of relevant models from NetBox
    })

    def __str__(self):
        return f"Requirements for {self.service_template.name}"


# Solution Deployment Model
class SolutionDeployment(NetBoxModel):
    solution_template = models.ForeignKey(SolutionTemplate, on_delete=models.CASCADE, related_name='deployments')
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)  # Refers to NetBox Tenant model
    deployment_date = models.DateTimeField()

    def __str__(self):
        return f"Deployment of {self.solution_template.name}"


# Service Deployment Model
class ServiceDeployment(NetBoxModel):
    service_template = models.ForeignKey(ServiceTemplate, on_delete=models.CASCADE, related_name='service_deployments')
    solution_deployment = models.ForeignKey(SolutionDeployment, on_delete=models.CASCADE, related_name='service_deployments')

    def __str__(self):
        return f"Service Deployment for {self.service_template.name}"


# Service Component Model
class ServiceComponent(NetBoxModel):
    service_deployment = models.ForeignKey(ServiceDeployment, on_delete=models.CASCADE, related_name='components')

    # Object type (GenericForeignKey) - allows dynamic references to any object type
    object_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('object_type', 'object_id')

    def __str__(self):
        return f"Component: {self.content_object} for {self.service_deployment}"


# High Availability (HA) Model
class HAModel(NetBoxModel):
    service_template = models.ForeignKey(ServiceTemplate, on_delete=models.CASCADE, related_name='ha_models')
    vip_required = models.BooleanField(default=False)
    primary_site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='primary_site')  # NetBox Site model
    secondary_site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='secondary_site')  # NetBox Site model
    tertiary_site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='tertiary_site')  # NetBox Site model
    replication = models.BooleanField(default=False)
    cluster = models.BooleanField(default=False)
    multi_site = models.BooleanField(default=False)
    snapshots = models.BooleanField(default=False)

    def __str__(self):
        return f"HA Model for {self.service_template.name}"


# Service Level Objective (SLO) Model
class SLO(NetBoxModel):
    service_template = models.ForeignKey(ServiceTemplate, on_delete=models.CASCADE, related_name='slos')
    rpo = models.IntegerField(help_text="Recovery Point Objective in hours")
    rto = models.IntegerField(help_text="Recovery Time Objective in hours")
    sev1_response = models.IntegerField(help_text="Severity 1 Response Time in minutes")
    sev2_response = models.IntegerField(help_text="Severity 2 Response Time in minutes")
    replicas_per_site = models.IntegerField()

    def __str__(self):
        return f"SLO for {self.service_template.name}"
