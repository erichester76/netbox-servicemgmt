from django.db import models
from netbox.models import NetBoxModel
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from tenancy.models import Tenant, Contact
from dcim.models import Site, Manufacturer
from taggit.managers import TaggableManager
from django.urls import reverse  # Import reverse


# Service Level Objective (SLO) Model
class SLO(NetBoxModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    rpo = models.IntegerField(help_text="Recovery Point Objective in hours", verbose_name='RPO (hours)')
    rto = models.IntegerField(help_text="Recovery Time Objective in hours", verbose_name='RTO (hours)')
    sev1_response = models.IntegerField(help_text="Severity 1 Response Time in minutes",null=True, blank=True, verbose_name='Severity 1 Respone Time (minutes)')
    sev2_response = models.IntegerField(help_text="Severity 2 Response Time in minutes",null=True, blank=True, verbose_name='Severity 2 Respone Time (minutes)')
    sev3_response = models.IntegerField(help_text="Severity 3 Response Time in minutes",null=True, blank=True, verbose_name='Severity 3 Respone Time (minutes)')

    class Meta:
        ordering = ['name']
        verbose_name = ('Service Level Object')
        verbose_name_plural = ('Service Level Objects')    

    def __str__(self):
        return f'{self.name}'
    
    def get_absolute_url(self):
        return reverse('plugins:netbox_servicemgmt:slo', kwargs={'pk': self.pk})
    
# Solution Template Model
class SolutionTemplate(NetBoxModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    design_contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True, related_name='solution_designers', verbose_name='Architect')
    requirements = models.TextField()

    def __str__(self):
        return f'{self.name}'
    
    def get_absolute_url(self):
        return reverse('plugins:netbox_servicemgmt:solutiontemplate', kwargs={'pk': self.pk})

# High Availability (HA) Model
class FaultTolerance(NetBoxModel):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    primary_site = models.ForeignKey(Site, on_delete=models.CASCADE, null=True, related_name='ft_primary_sites')
    secondary_site = models.ForeignKey(Site, on_delete=models.CASCADE, null=True, blank=True, related_name='ft_secondary_sites')
    tertiary_site = models.ForeignKey(Site, on_delete=models.CASCADE, null=True, blank=True, related_name='ft_tertiary_sites')  
    instances_per_site = models.IntegerField(null=True)
    vip_required = models.BooleanField(null=True)
    offsite_replication = models.BooleanField(null=True)
    clustered = models.BooleanField(null=True)
    multi_site = models.BooleanField(null=True)
    multi_region = models.BooleanField(null=True)
    snapshots = models.BooleanField(null=True)
    backup_schedule = models.CharField(max_length=255, null=True)
    offsite_backup = models.BooleanField(null=True)
    airgap_backup = models.BooleanField(null=True)

    class Meta:
        ordering = ['name']
        verbose_name = ('Fault Tolerence Model')
        verbose_name_plural = ('Fault Tolerence Models')    
    
    def __str__(self):
        return f'{self.name}'
    
    def get_absolute_url(self):
        return reverse('plugins:netbox_servicemgmt:faulttolerance', kwargs={'pk': self.pk})


# Service Template Model
class ServiceTemplate(NetBoxModel):
    
    name = models.CharField(max_length=255)
    description = models.TextField()
    solution_template = models.ForeignKey(SolutionTemplate, on_delete=models.CASCADE, null=True, related_name='st_solutions', verbose_name='Solution Template')
    design_contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True, related_name='service_designers', verbose_name='Architect')
    service_type = models.CharField(max_length=255)
    vendor_management_assessment = models.CharField(max_length=255)
    vendor = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, null=True, related_name='st_vendor', verbose_name='Vendor')

    #fault tolerence defaults, can be overridden at servicerequirement level
    fault_tolerence = models.ForeignKey(FaultTolerance, on_delete=models.CASCADE, related_name='st_ft', verbose_name='Assigned Fault Tolerance Profile')
    #slo defaults, can be overridden at servicerequirement level
    service_slo = models.ForeignKey(SLO, on_delete=models.CASCADE, null=True, related_name='st_slo', verbose_name='Assigned Service Level Object Profile')

    #to fix conflict with ipam service templates
    tags = TaggableManager(related_name='netbox_servicemgmt_servicetemplates')

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_servicemgmt:servicetemplate', kwargs={'pk': self.pk})

# Service Requirement Model
class ServiceRequirement(NetBoxModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    
    service_template = models.ForeignKey(ServiceTemplate, on_delete=models.CASCADE, related_name='service_requirements', verbose_name='Service Template')
    requirement_owner = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True, related_name='sr_designers', verbose_name='Requirement Owner')

    #overrides for service template slo
    service_slo = models.ForeignKey(SLO, on_delete=models.CASCADE, null=True, related_name='sr_slo',verbose_name='Assigned SLO Profile')
    
    #overrides for fault tolerence at service template level
    primary_site = models.ForeignKey(Site, on_delete=models.CASCADE, null=True, blank=True, related_name='sr_primary_site_overrides')
    secondary_site = models.ForeignKey(Site, on_delete=models.CASCADE, null=True, blank=True, related_name='sr_secondary_site_overrides')
    tertiary_site = models.ForeignKey(Site, on_delete=models.CASCADE, null=True, blank=True, related_name='sr_tertiary_site_overrrides')  
    instances_per_site = models.IntegerField(null=True, blank=True)
    vip_required = models.BooleanField(null=True, blank=True)
    offsite_replication = models.BooleanField(null=True, blank=True)
    clustered = models.BooleanField(null=True, blank=True)
    multi_site = models.BooleanField(null=True, blank=True)
    multi_region = models.BooleanField(null=True, blank=True)
    snapshots = models.BooleanField(null=True, blank=True)
    backup_schedule = models.CharField(max_length=255, null=True, blank=True)
    offsite_backup = models.BooleanField(null=True, blank=True)
    airgap_backup = models.BooleanField(null=True, blank=True)
    
    # Object Type field to link to any NetBox object type
    object_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)    

    # Enumerated requirement fields (these will be fields from the referenced object to set defaults for deployment)
    requirement1_field = models.CharField(max_length=255, null=True, blank=True)
    requirement1_value = models.CharField(max_length=255, null=True, blank=True)
    requirement2_field = models.CharField(max_length=255, null=True, blank=True)
    requirement2_value = models.CharField(max_length=255, null=True, blank=True)
    requirement3_field = models.CharField(max_length=255, null=True, blank=True)
    requirement3_value = models.CharField(max_length=255, null=True, blank=True)
    requirement4_field = models.CharField(max_length=255, null=True, blank=True)
    requirement4_value = models.CharField(max_length=255, null=True, blank=True)
    requirement5_field = models.CharField(max_length=255, null=True, blank=True)
    requirement5_value = models.CharField(max_length=255, null=True, blank=True)
    requirement6_field = models.CharField(max_length=255, null=True, blank=True)
    requirement6_value = models.CharField(max_length=255, null=True, blank=True)
    requirement7_field = models.CharField(max_length=255, null=True, blank=True)
    requirement7_value = models.CharField(max_length=255, null=True, blank=True)
    requirement8_field = models.CharField(max_length=255, null=True, blank=True)
    requirement8_value = models.CharField(max_length=255, null=True, blank=True)
    requirement9_field = models.CharField(max_length=255, null=True, blank=True)
    requirement9_value = models.CharField(max_length=255, null=True, blank=True)
    requirement10_field = models.CharField(max_length=255, null=True, blank=True)
    requirement10_value = models.CharField(max_length=255, null=True, blank=True)
    requirement11_field = models.CharField(max_length=255, null=True, blank=True)
    requirement11_value = models.CharField(max_length=255, null=True, blank=True)
    requirement12_field = models.CharField(max_length=255, null=True, blank=True)
    requirement12_value = models.CharField(max_length=255, null=True, blank=True)
    requirement13_field = models.CharField(max_length=255, null=True, blank=True)
    requirement13_value = models.CharField(max_length=255, null=True, blank=True)
    requirement14_field = models.CharField(max_length=255, null=True, blank=True)
    requirement14_value = models.CharField(max_length=255, null=True, blank=True)
    requirement15_field = models.CharField(max_length=255, null=True, blank=True)
    requirement15_value = models.CharField(max_length=255, null=True, blank=True)
    requirement16_field = models.CharField(max_length=255, null=True, blank=True)
    requirement16_value = models.CharField(max_length=255, null=True, blank=True)
    requirement17_field = models.CharField(max_length=255, null=True, blank=True)
    requirement17_value = models.CharField(max_length=255, null=True, blank=True)
    requirement18_field = models.CharField(max_length=255, null=True, blank=True)
    requirement18_value = models.CharField(max_length=255, null=True, blank=True)
    requirement19_field = models.CharField(max_length=255, null=True, blank=True)
    requirement19_value = models.CharField(max_length=255, null=True, blank=True)
    requirement20_field = models.CharField(max_length=255, null=True, blank=True)
    requirement20_value = models.CharField(max_length=255, null=True, blank=True)
    
    
    def __str__(self):
        return f'{self.name}'
        
    def get_absolute_url(self):
        return reverse('plugins:netbox_servicemgmt:servicerequirement', kwargs={'pk': self.pk})    


# Solution Deployment Model
class SolutionDeployment(NetBoxModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    solution_template = models.ForeignKey(SolutionTemplate, on_delete=models.CASCADE, related_name='solution_deployments', verbose_name='Solution Template')
    deployment_type = models.CharField(max_length=255, null=True, blank=True)
    deployment_date = models.DateTimeField()

    def __str__(self):
        return f'{self.name}'
        
    def get_absolute_url(self):
        return reverse('plugins:netbox_servicemgmt:solutiondeployment', kwargs={'pk': self.pk})


# Service Deployment Model
class ServiceDeployment(NetBoxModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    service_template = models.ForeignKey(ServiceTemplate, on_delete=models.CASCADE, related_name='service_deployments',  verbose_name='Service Template')
    solution_deployment = models.ForeignKey(SolutionDeployment, on_delete=models.CASCADE, related_name='service_deployments', verbose_name='Solution Deployment')
    production_readiness_checklist = models.CharField(max_length=255, null=True, blank=True, verbose_name='Production Readiness Checklist')   
    business_owner_tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True,related_name='sd_business_owners', verbose_name='Business Owner Contact')
    business_owner_contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True,related_name='sd_business_owners', verbose_name='Business Owner Department')
    service_owner_contact  = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True,related_name='sd_service_owners', verbose_name='Service Owner Contact')
    service_owner_tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True,related_name='sd_service_owners', verbose_name='Service Owner Department')
    major_incident_coordinator_contact  = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True,related_name='sd_mi_owners', verbose_name='Major Incident Contact')
    functional_area_sponsor_tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True,related_name='sd_fa_owners', verbose_name='Functional Area Sponsor')
    functional_sub_area_sponsor_tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True,related_name='sd_sfa_owners', verbose_name='Functional Sub-Area Sponsor')
    engineering_contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True, related_name='sd_responsible_deployment', verbose_name='Deployment Contact')
    operations_contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True, related_name='sd_responsible_operations', verbose_name='Operations Contact')
    monitoring_contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True, related_name='sd_responsible_monitoring', verbose_name='Monitoring Contact')
    maintenance_window = models.CharField(max_length=255, verbose_name='Maintenance Window Timeframes')
    deployment_rfc = models.CharField(max_length=255, verbose_name='Associated RFC for Deployment')
    
    def __str__(self):
        return f'{self.name}'   
    
    def get_absolute_url(self):
        return reverse('plugins:netbox_servicemgmt:servicedeployment', kwargs={'pk': self.pk})


# Service Component Model
class ServiceComponent(NetBoxModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    service_deployment = models.ForeignKey(ServiceDeployment, on_delete=models.CASCADE, related_name='sc_components', verbose_name='Service Deployment')
    service_requirement = models.ForeignKey(ServiceRequirement, on_delete=models.CASCADE, related_name='sc_components', verbose_name='Service Requirement')

    # Object type (GenericForeignKey) - allows dynamic references to any object type
    object_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('object_type', 'object_id')

    class Meta:
        ordering = ['name']
        verbose_name = ('Deployment Component')
        verbose_name_plural = ('Deployment Components')
    
    @property
    def content_object_verbose_name(self):
        """ Returns a human-readable name for the related content object based on its type """
        if self.object_type:
            return self.object_type
        return None
    
    def __str__(self):
        return f'{self.name}'    
    
    def get_absolute_url(self):
        return reverse('plugins:netbox_servicemgmt:servicecomponent', kwargs={'pk': self.pk})