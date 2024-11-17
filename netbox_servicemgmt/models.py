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

SOLUTION_APP_PREMISE = 'applicationpremise'
SOLUTION_APP_CLOUD = 'applicationcloud'
SOLUTION_APP_SASS = 'applicationsaas'
SOLUTION_APP_HYBRID = 'applicationhybrid'
SOLUTION_INFRA = 'infrastructure'
SOLUTION_SERVICE = 'service'

SOLUTION_CHOICES = [
    {SOLUTION_APP_PREMISE, 'On Premise Application'},
    {SOLUTION_APP_CLOUD, 'Cloud Hosted Application'},
    {SOLUTION_APP_SASS, 'SaaS Application'},
    {SOLUTION_APP_HYBRID, 'Hybrid Application'},
    {SOLUTION_INFRA,  'Infrastructure'},
    {SOLUTION_SERVICE, 'Contracted Service'}
]

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
    slo = models.ForeignKey(SLO, on_delete=models.SET_NULL, null=True, related_name='sla_slo',verbose_name='Assigned SLO Profile')
    business_owner_tenant = models.ForeignKey(Tenant, on_delete=models.SET_NULL, null=True,related_name='sla_business_owners', verbose_name='Business Owner Department')
    business_owner_contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True,related_name='sla_business_owners', verbose_name='Business Owner Contact')
    technical_contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True,related_name='sla_technical_contacts', verbose_name='Technical Contact')
    data_classification = models.CharField(max_length=20,choices=DATA_CHOICES)
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
    primary_site = models.ForeignKey(Site, on_delete=models.SET_NULL, null=True, related_name='ft_primary_sites')
    secondary_site = models.ForeignKey(Site, on_delete=models.SET_NULL, null=True, blank=True, related_name='ft_secondary_sites')
    tertiary_site = models.ForeignKey(Site, on_delete=models.SET_NULL, null=True, blank=True, related_name='ft_tertiary_sites')  
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
    description = models.TextField(blank=True, null=True)
    design_contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True, related_name='sor_designers', verbose_name='Architect')
    business_owner_tenant = models.ForeignKey(Tenant, on_delete=models.SET_NULL, blank=True, null=True,related_name='sor_business_owners', verbose_name='Business Owner Department')
    business_owner_contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, blank=True, null=True,related_name='sor_business_owners', verbose_name='Business Owner Contact')
    service_owner_tenant = models.ForeignKey(Tenant, on_delete=models.SET_NULL, blank=True, null=True,related_name='sor_service_owners', verbose_name='Service Owner Department')
    service_owner_contact  = models.ForeignKey(Contact, on_delete=models.SET_NULL, blank=True, null=True,related_name='sor_service_owners', verbose_name='Service Owner Contact')
    functional_area_sponsor_tenant = models.ForeignKey(Tenant, on_delete=models.SET_NULL, blank=True, null=True,related_name='sor_fa_owners', verbose_name='Functional Area Sponsor')
    functional_sub_area_sponsor_tenant = models.ForeignKey(Tenant, on_delete=models.SET_NULL, blank=True, null=True,related_name='sor_sfa_owners', verbose_name='Functional Sub-Area Sponsor')
    solution_type = models.CharField(max_length=55, null=True, choices=SOLUTION_CHOICES)
    version = models.IntegerField(null=True, blank=True)
    slo = models.ForeignKey(SLO, on_delete=models.SET_NULL, blank=True, null=True, related_name='sor_slo',verbose_name='Assigned SLO Profile')
    data_classification = models.CharField(null=True, blank=True, choices=DATA_CHOICES)
    clustered = models.BooleanField(blank=True,null=True)
    multi_site = models.BooleanField(blank=True,null=True)
    multi_region = models.BooleanField(blank=True,null=True)
    offsite_replication = models.BooleanField(blank=True,null=True)
    offsite_backup = models.BooleanField(blank=True,null=True)
    airgap_backup = models.BooleanField(blank=True,null=True)
    rfp_ref = models.TextField(blank=True, null=True)
    rfp_status = models.TextField(blank=True, null=True, choices=REQUEST_CHOICES)

    requirements = models.TextField(null=True, blank=True, verbose_name='Additional Requirements')

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
    design_contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True, related_name='sot_designers', verbose_name='Architect')
    solution_type = models.CharField(max_length=55, null=True, choices=SOLUTION_CHOICES)
    version = models.IntegerField(null=True, blank=True)
    vendors = models.ManyToManyField(Manufacturer, blank=True, null=True, related_name='sot_vendors', verbose_name='Vendors')
    sla_number = models.CharField(max_length=50, null=True)
    slo = models.ForeignKey(SLO, on_delete=models.SET_NULL, null=True, related_name='sot_slo',verbose_name='Assigned SLO Profile')
    data_classification = models.CharField(null=True,choices=DATA_CHOICES)
    fault_tolerence = models.ForeignKey(FaultTolerance, on_delete=models.SET_NULL, null=True, related_name='sot_slo',verbose_name='Assigned SLO Profile')
    solution_request = models.ForeignKey(SolutionRequest, on_delete=models.SET_NULL, null=True, related_name='sot_sr',verbose_name='Assigned SLO Profile')
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
    version = models.IntegerField(null=True, blank=True)
    
    # Self-referencing foreign key to track the previous version of the template
    previous_version = models.ForeignKey(
        'self',  # Self-reference to the same model
        on_delete=models.SET_NULL,  # Allow deletion without deleting related records
        null=True,  # Previous version can be optional (i.e., the first version will have no previous_version)
        blank=True,
        related_name='next_versions',  # Allows backward reference from the newer version to older ones
        help_text="Previous version of this service"
    )

    
    fault_tolerence = models.ForeignKey(FaultTolerance, null=True, on_delete=models.SET_NULL, related_name='st_ft', verbose_name='Assigned Fault Tolerance Profile')
    service_slo = models.ForeignKey(SLO, on_delete=models.SET_NULL, null=True, related_name='st_slo', verbose_name='Assigned Service Level Object Profile')
    
    vendor = models.ForeignKey(Manufacturer, on_delete=models.SET_NULL, null=True, related_name='st_vendor', verbose_name='Vendor')
    vendor_management_status = models.TextField(null=True, choices=REVIEW_CHOICES)
    vendor_management_number = models.CharField(max_length=50, null=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,  
        default=STATUS_INACTIVE,   
    )
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
    service_template = models.ForeignKey(ServiceTemplate, null=True, on_delete=models.SET_NULL, related_name='service_requirements', verbose_name='Service Template')
    requirement_owner = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True, related_name='sr_designers', verbose_name='Requirement Owner')
    fault_tolerence = models.ForeignKey(FaultTolerance, null=True, on_delete=models.SET_NULL, related_name='sr_ft', verbose_name='Assigned Fault Tolerance Profile')
    service_slo = models.ForeignKey(SLO, on_delete=models.SET_NULL, null=True, related_name='sr_slo',verbose_name='Assigned SLO Profile')
    version = models.IntegerField(null=True, blank=True)
    
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
        null=True,
        on_delete=models.SET_NULL, 
        limit_choices_to={'model__in': ['device', 'virtualmachine', 'softwareproduct', 'ipaddress', 'hostname', 'certificate', 'lbvirtualserver', 'container']},  # Filter by model names
        verbose_name="Attached Component Type"
    )
   
    def __str__(self):
        return f'{self.name}'
        
    def get_absolute_url(self):
        return reverse('plugins:netbox_servicemgmt:servicerequirement', kwargs={'pk': self.pk})    


# Service Deployment Model
class ServiceDeployment(NetBoxModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    service_template = models.ForeignKey(ServiceTemplate, null=True, on_delete=models.SET_NULL, related_name='service_deployments',  verbose_name='Service Template')
    production_readiness_checklist = models.CharField(max_length=255, null=True, blank=True, verbose_name='Production Readiness Checklist')   
    deployment_rfc = models.CharField(max_length=255, verbose_name='Associated RFC for Deployment')
    major_incident_coordinator_contact  = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True,related_name='sd_mi_owners', verbose_name='Major Incident Contact')
    engineering_contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True, related_name='sd_responsible_deployment', verbose_name='Deployment Contact')
    operations_contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True, related_name='sd_responsible_operations', verbose_name='Operations Contact')
    monitoring_contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True, related_name='sd_responsible_monitoring', verbose_name='Monitoring Contact')
    maintenance_window = models.CharField(max_length=255, verbose_name='Maintenance Window Timeframes')
    version = models.IntegerField(null=True, blank=True)
    
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
    service_requirement = models.ForeignKey(ServiceRequirement, null=True, on_delete=models.SET_NULL, related_name='sc_components', verbose_name='Service Requirement')
    service_deployment = models.ForeignKey(ServiceDeployment, null=True, on_delete=models.SET_NULL, related_name='sc_deployments', verbose_name='Service Deployment')
    # Object type (GenericForeignKey) - allows dynamic references to any object type
    object_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('object_type', 'object_id')
    version = models.IntegerField(null=True, blank=True)
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