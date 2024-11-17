from django.db import models
from netbox.models import NetBoxModel
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from tenancy.models import Tenant, Contact
from dcim.models import Site, Manufacturer
from taggit.managers import TaggableManager
from virtualization.models import VirtualMachine
from django.urls import reverse  # Import reverse

# Status choices
STATUS_INACTIVE = 'inactive'
STATUS_ACTIVE = 'active'
STATUS_STAGED = 'staged'
STATUS_TESTING = 'testing'
STATUS_DETECTED = 'detected'
STATUS_REPLACED = 'replaced'
STATUS_DECOMMISSIONED = 'decommissioned'
STATUS_NONE = 'none'
STATUS_PLANNING = 'planning'
STATUS_DRAFT = 'draft'
STATUS_SUBMITTED = 'submitted'
STATUS_BID = 'outforbid'
STATUS_AWARDED = 'awarded'
STATUS_REVIEW = 'awarded'
STATUS_COMPLETE = 'awarded'

STATUS_CHOICES = [
    (STATUS_INACTIVE, 'inactive'),
    (STATUS_ACTIVE, 'active'),
    (STATUS_PLANNING, 'planning'),
    (STATUS_STAGED, 'staged'),
    (STATUS_TESTING, 'testing'),
    (STATUS_REPLACED, 'replaced'),
    (STATUS_DECOMMISSIONED, 'decommissioned'),
]

REQUEST_CHOICES = [
    (STATUS_NONE, 'None'),
    (STATUS_PLANNING, 'Planning'),
    (STATUS_DRAFT, 'Draft'),
    (STATUS_SUBMITTED, 'Submitted'),
    (STATUS_BID, 'Out for Bids'),
    (STATUS_AWARDED, 'Awarded'),
]

REVIEW_CHOICES = [
    (STATUS_NONE, 'None'),
    (STATUS_DRAFT, 'Draft'),
    (STATUS_SUBMITTED, 'Submitted'),
    (STATUS_REVIEW, 'Under Review'),
    (STATUS_COMPLETE, 'COmplete'),
]   

# Status choices
DATA_PUBLIC = 'public'
DATA_INTERNAL = 'internal_use'
DATA_CONFIDENTIAL = 'confidential'
DATA_RESTRICTED= 'restricted'

DATA_CHOICES = [
    (DATA_PUBLIC, 'Public'),
    (DATA_INTERNAL, 'Internal Use'),
    (DATA_CONFIDENTIAL, 'Confidential'),
    (DATA_RESTRICTED, 'Restricted'),
]
    

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
 
 # Service Level Objective (SLA) Model
class SLA(NetBoxModel):
    name = models.CharField(max_length=255)
    uuid = models.CharField(max_length=30, null=True)
    description = models.TextField()
    slo = models.ForeignKey(SLO, on_delete=models.CASCADE, null=True, related_name='sla_slo',verbose_name='Assigned SLO Profile')
    business_owner_tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True,related_name='sla_business_owners', verbose_name='Business Owner Department')
    business_owner_contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True,related_name='sla_business_owners', verbose_name='Business Owner Contact')
    technical_contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True,related_name='sla_technical_contacts', verbose_name='Technical Contact')
    data_classification = models.CharField(
        max_length=20,
        choices=DATA_CHOICES,  
    )
    virtual_machines = models.ManyToManyField(
        VirtualMachine,
        related_name='sla',
        blank=True
    )
    
    class Meta:
        ordering = ['name']
        verbose_name = ('Service Level Agreement')
        verbose_name_plural = ('Service Level Agreements')    

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_servicemgmt:sla', kwargs={'pk': self.pk})


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


# Solution Request Model
class SolutionRequest(NetBoxModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    design_contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True, related_name='sreq_designers', verbose_name='Architect')
    business_owner_tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True,related_name='sreq_business_owners', verbose_name='Business Owner Department')
    business_owner_contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True,related_name='sreq_business_owners', verbose_name='Business Owner Contact')
    solution_type = models.CharField(max_length=255, null=True)
    version = models.CharField(max_length=50, null=True, help_text="Version of the solution request")
    vendors = models.ManyToManyRel(Manufacturer, null=True, related_name='sreq_vendors', verbose_name='Vendors')
    sla_number = models.CharField(max_length=50, null=True)
    vendor_management_number = models.CharField(max_length=50, null=True)
    slo = models.ForeignKey(SLO, on_delete=models.CASCADE, null=True, related_name='sr_slo',verbose_name='Assigned SLO Profile')
    data_classification = models.CharField(null=True,choices=DATA_CHOICES)
    clustered = models.BooleanField(null=True)
    multi_site = models.BooleanField(null=True)
    multi_region = models.BooleanField(null=True)
    offsite_replication = models.BooleanField(null=True)
    offsite_backup = models.BooleanField(null=True)
    airgap_backup = models.BooleanField(null=True)
    rfp_status = models.TextField(null=True,choices=REQUEST_CHOICES)
    vendor_managment_status = models.TextField(null=True,choices=REVIEW_CHOICES)
    requirements = models.TextField(null=True,Blank=True,verbose_name='Additional Requirements')

    # Self-referencing foreign key to track the previous version of the template
    previous_version = models.ForeignKey(
        'self',  # Self-reference to the same model
        on_delete=models.SET_NULL,  # Allow deletion without deleting related records
        null=True,  # Previous version can be optional (i.e., the first version will have no previous_version)
        blank=True,
        related_name='next_versions',  # Allows backward reference from the newer version to older ones
        help_text="Previous version of this solution"
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,  
        default=STATUS_INACTIVE,    
    )
    
    class Meta:
        ordering = ['name']
        verbose_name = ('Solution Request')
        verbose_name_plural = ('Solution Requests') 

    def __str__(self):
        return f'{self.name}'
    
    def get_absolute_url(self):
        return reverse('plugins:netbox_servicemgmt:solutionrequest', kwargs={'pk': self.pk})
 
# Solution Template Model
class SolutionTemplate(NetBoxModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    design_contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True, related_name='sreq_designers', verbose_name='Architect')
    business_owner_tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True,related_name='sreq_business_owners', verbose_name='Business Owner Department')
    business_owner_contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True,related_name='sreq_business_owners', verbose_name='Business Owner Contact')
    solution_type = models.CharField(max_length=255, null=True)
    version = models.CharField(max_length=50, null=True, help_text="Version of the solution request")
    vendors = models.ManyToManyRel(Manufacturer, null=True, related_name='sreq_vendors', verbose_name='Vendors')
    sla_number = models.CharField(max_length=50, null=True)
    slo = models.ForeignKey(SLO, on_delete=models.CASCADE, null=True, related_name='sr_slo',verbose_name='Assigned SLO Profile')
    data_classification = models.CharField(null=True,choices=DATA_CHOICES)
    fault_tolerance = models.ForeignKey(FaultTolerance, on_delete=models.CASCADE, null=True, related_name='sr_slo',verbose_name='Assigned SLO Profile')
        
    # Self-referencing foreign key to track the previous version of the template
    previous_version = models.ForeignKey(
        'self',  # Self-reference to the same model
        on_delete=models.SET_NULL,  # Allow deletion without deleting related records
        null=True,  # Previous version can be optional (i.e., the first version will have no previous_version)
        blank=True,
        related_name='next_versions',  # Allows backward reference from the newer version to older ones
        help_text="Previous version of this solution"
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,  
        default=STATUS_INACTIVE,    
    )
    class Meta:
        ordering = ['name']
        verbose_name = ('Solution')
        verbose_name_plural = ('Solutions') 

    def __str__(self):
        return f'{self.name}'
    
    def get_absolute_url(self):
        return reverse('plugins:netbox_servicemgmt:solutiontemplate', kwargs={'pk': self.pk})


# Service Template Model
class ServiceTemplate(NetBoxModel):
    
    name = models.CharField(max_length=255)
    description = models.TextField()
    solution_templates = models.ManyToManyField(
        'SolutionTemplate', 
        related_name='service_templates', 
        verbose_name='Solution Templates'
    )    
    design_contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True, related_name='service_designers', verbose_name='Architect')
    service_type = models.CharField(max_length=255)
    vendor_management_assessment = models.CharField(max_length=255)
    vendor = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, null=True, related_name='st_vendor', verbose_name='Vendor')
    version = models.CharField(max_length=50, null=True, help_text="Version of the service")
    
    # Self-referencing foreign key to track the previous version of the template
    previous_version = models.ForeignKey(
        'self',  # Self-reference to the same model
        on_delete=models.SET_NULL,  # Allow deletion without deleting related records
        null=True,  # Previous version can be optional (i.e., the first version will have no previous_version)
        blank=True,
        related_name='next_versions',  # Allows backward reference from the newer version to older ones
        help_text="Previous version of this service"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,  
        default=STATUS_INACTIVE,   
    )
    
    #fault tolerence defaults, can be overridden at servicerequirement level
    fault_tolerence = models.ForeignKey(FaultTolerance, on_delete=models.CASCADE, related_name='st_ft', verbose_name='Assigned Fault Tolerance Profile')
    #slo defaults, can be overridden at servicerequirement level
    service_slo = models.ForeignKey(SLO, on_delete=models.CASCADE, null=True, related_name='st_slo', verbose_name='Assigned Service Level Object Profile')

    #to fix conflict with ipam service templates
    tags = TaggableManager(related_name='netbox_servicemgmt_servicetemplates')

    class Meta:
        ordering = ['name']
        verbose_name = ('Service')
        verbose_name_plural = ('Services') 

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
    version = models.CharField(max_length=50, null=True, help_text="Version of the solution template")
    
    # Self-referencing foreign key to track the previous version of the template
    previous_version = models.ForeignKey(
        'self',  # Self-reference to the same model
        on_delete=models.SET_NULL,  # Allow deletion without deleting related records
        null=True,  # Previous version can be optional (i.e., the first version will have no previous_version)
        blank=True,
        related_name='next_versions',  # Allows backward reference from the newer version to older ones
        help_text="Previous version of this requirement"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,  
        default=STATUS_INACTIVE,   
    )
    
    # Object Type field to link to any NetBox object type
    object_type = models.ForeignKey(
        ContentType, 
        on_delete=models.CASCADE, 
        limit_choices_to={'model__in': ['device', 'virtualmachine', 'softwareproduct', 'ipaddress', 'hostname', 'certificate', 'lbvirtualserver', 'container']},  # Filter by model names
        verbose_name="Attached Component Type"
    )
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


# Service Deployment Model
class ServiceDeployment(NetBoxModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    service_template = models.ForeignKey(ServiceTemplate, on_delete=models.CASCADE, related_name='service_deployments',  verbose_name='Service Template')
    production_readiness_checklist = models.CharField(max_length=255, null=True, blank=True, verbose_name='Production Readiness Checklist')   
    business_owner_tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True,related_name='sd_business_owners', verbose_name='Business Owner Department')
    business_owner_contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True,related_name='sd_business_owners', verbose_name='Business Owner Contact')
    service_owner_tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True,related_name='sd_service_owners', verbose_name='Service Owner Department')
    service_owner_contact  = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True,related_name='sd_service_owners', verbose_name='Service Owner Contact')
    functional_area_sponsor_tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True,related_name='sd_fa_owners', verbose_name='Functional Area Sponsor')
    functional_sub_area_sponsor_tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True,related_name='sd_sfa_owners', verbose_name='Functional Sub-Area Sponsor')
    major_incident_coordinator_contact  = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True,related_name='sd_mi_owners', verbose_name='Major Incident Contact')
    engineering_contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True, related_name='sd_responsible_deployment', verbose_name='Deployment Contact')
    operations_contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True, related_name='sd_responsible_operations', verbose_name='Operations Contact')
    monitoring_contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True, related_name='sd_responsible_monitoring', verbose_name='Monitoring Contact')
    maintenance_window = models.CharField(max_length=255, verbose_name='Maintenance Window Timeframes')
    deployment_rfc = models.CharField(max_length=255, verbose_name='Associated RFC for Deployment')
    version = models.CharField(max_length=50, null=True, help_text="Version of the deployment")
    
    # Self-referencing foreign key to track the previous version of the template
    previous_version = models.ForeignKey(
        'self',  # Self-reference to the same model
        on_delete=models.SET_NULL,  # Allow deletion without deleting related records
        null=True,  # Previous version can be optional (i.e., the first version will have no previous_version)
        blank=True,
        related_name='next_versions',  # Allows backward reference from the newer version to older ones
        help_text="Previous version of this deployment"
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,  
        default=STATUS_INACTIVE,   
    )

    def __str__(self):
        return f'{self.name}'   
    
    def get_absolute_url(self):
        return reverse('plugins:netbox_servicemgmt:servicedeployment', kwargs={'pk': self.pk})


# Service Component Model
class ServiceComponent(NetBoxModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    service_requirement = models.ForeignKey(ServiceRequirement, on_delete=models.CASCADE, related_name='sc_components', verbose_name='Service Requirement')
    service_deployment = models.ForeignKey(ServiceDeployment, on_delete=models.CASCADE, related_name='sc_deployments', verbose_name='Service Deployment')
    # Object type (GenericForeignKey) - allows dynamic references to any object type
    object_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('object_type', 'object_id')
    version = models.CharField(max_length=50, null=True, help_text="Version of the Component")
    # Self-referencing foreign key to track the previous version of the template
    previous_version = models.ForeignKey(
        'self',  # Self-reference to the same model
        on_delete=models.SET_NULL,  # Allow deletion without deleting related records
        null=True,  # Previous version can be optional (i.e., the first version will have no previous_version)
        blank=True,
        related_name='next_versions',  # Allows backward reference from the newer version to older ones
        help_text="Previous version of this Component"
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,  
        default=STATUS_INACTIVE,   
    )
    
    class Meta:
        ordering = ['name']
        verbose_name = ('Deployment Component')
        verbose_name_plural = ('Deployment Components')
    
    @property
    def content_object_verbose_name(self):
        """ Returns a human-readable name for the related content object based on its type """
        if self.object_type:
            return self.object_type._meta.object_name
        return None
    
    def __str__(self):
        return f'{self.name}'    
    
    def get_absolute_url(self):
        return reverse('plugins:netbox_servicemgmt:servicecomponent', kwargs={'pk': self.pk})