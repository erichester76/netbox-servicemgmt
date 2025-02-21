from django.db import models
from netbox.models import NetBoxModel
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from tenancy.models import Tenant, Contact
from dcim.models import Site
from ipam.models import VLAN, Prefix
from django.urls import reverse
from netbox.models.features import *


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
STATUS_REVIEW = 'review'
STATUS_COMPLETE = 'complete'

DATA_PUBLIC = 'public'
DATA_INTERNAL = 'internal_use'
DATA_CONFIDENTIAL = 'confidential'
DATA_RESTRICTED= 'restricted'

SOLUTION_APP_PREMISE = 'applicationpremise'
SOLUTION_APP_CLOUD = 'applicationcloud'
SOLUTION_APP_SASS = 'applicationsaas'
SOLUTION_APP_HYBRID = 'applicationhybrid'
SOLUTION_INFRA = 'infrastructure'
SOLUTION_SERVICE = 'service'


SOLUTION_CHOICES = [
    (SOLUTION_APP_PREMISE, 'On Premise Application'),
    (SOLUTION_APP_CLOUD, 'Cloud Hosted Application'),
    (SOLUTION_APP_SASS, 'SaaS Application'),
    (SOLUTION_APP_HYBRID, 'Hybrid Application'),
    (SOLUTION_INFRA,  'Infrastructure'),
    (SOLUTION_SERVICE, 'Contracted Service')
]

DATA_CHOICES = [
    (DATA_PUBLIC, 'Public'),
    (DATA_INTERNAL, 'Internal Use'),
    (DATA_CONFIDENTIAL, 'Confidential'),
    (DATA_RESTRICTED, 'Restricted'),
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

COMPLIANCE_STANDARDS = [
    ('ISO 27001', 'ISO 27001'),
    ('ISO 27002', 'ISO 27002'),
    ('FERPA', 'FERPA'),
    ('FISMA', 'FISMA'),
    ('HIPAA', 'HIPAA'),
    ('PCI DSS', 'PCI DSS'),
    ('CMMC', 'CMMC'),          
    ('SOC 2', 'SOC 2'),
    ('SOX', 'Sarbanes-Oxley'),
    ('FedRAMP', 'FedRAMP'),
    ('FIPS 140-2', 'FIPS 140-2'),
    ('GDPR', 'GDPR'),
    ('NIST 800-53', 'NIST 800-53'),
    ('NIST 800-171', 'NIST 800-171'),
    ('NIST CSF', 'NIST CSF'),
    ('CIS Controls', 'CIS Controls'),
]

DEPLOYMENT_TYPES = [
    ('p','Production'),
    ('g','Upgrade'),
    ('q','Quality Assurance'),
    ('u','User Acceptance Testing (UAT)'),
    ('d','Development'),
    ('s','Staging'),
    ('y','Prototype'),
    ('l','Learning/Training'),
    ('m','(Maintenance) Production Support'),
    ('n','Non-production'),
    ('f','Functional'),
    ('r','Disaster Recovery'),
    ('c','Secondary/Failover'),
    ('z','Sandbox'),
    ('o','Demo'),
]

class DynamicQuerySetModel:
    """
    A utility to dynamically generate a queryset and API URL
    based on the selected content type.
    """
    def __init__(self, object_type=None):
        self.object_type = object_type

    @property
    def queryset(self):
        """Return the queryset for the selected content type."""
        if self.object_type:
            model_class = ContentType.objects.get(pk=self.object_type).model_class()
            if model_class:
                return model_class.objects.all()
        return Component.objects.none()  # Return empty set if no object_type is set

    @property
    def get_absolute_url(self):
        """Return the API URL for the selected content type."""
        if self.object_type:
            model_class = ContentType.objects.get(pk=self.object_type).model_class()
            if model_class:
                return reverse(
                    f'{model_class._meta.app_label}:{model_class._meta.model_name}'
                )
        return Component.objects.none()  # Return empty set if no object_type is set


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
        return reverse('plugins:netbox_sm:slo', kwargs={'pk': self.pk})
 
# High Availability (HA) Model
class FaultTolerence(NetBoxModel):

    name = models.CharField(max_length=255)
    description = models.TextField(null=True)

    multi_site = models.BooleanField(null=True)
    multi_region = models.BooleanField(null=True)
    multi_cloud = models.BooleanField(null=True)
    
    primary_site = models.ForeignKey(Site, on_delete=models.SET_NULL, null=True, related_name='ft_primary_sites')
    secondary_site = models.ForeignKey(Site, on_delete=models.SET_NULL, null=True, blank=True, related_name='ft_secondary_sites')
    tertiary_site = models.ForeignKey(Site, on_delete=models.SET_NULL, null=True, blank=True, related_name='ft_tertiary_sites')  

    gtm_required = models.BooleanField(null=True)
    ltm_required = models.BooleanField(null=True)

    snapshots = models.BooleanField(null=True)
    storage_replication = models.BooleanField(null=True)
    vm_replication = models.BooleanField(null=True)
    backups = models.BooleanField(null=True)

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
        return reverse('plugins:netbox_sm:faulttolerence', kwargs={'pk': self.pk})

class Solution(NetBoxModel):

    name = models.CharField(max_length=255)
    solution_number = models.CharField(max_length=50, null=True, verbose_name='Billing Number')
    project_id = models.CharField(max_length=50, null=True) # 4gj-sis
    
    description = models.TextField()
    solution_type = models.CharField(max_length=55, null=True, choices=SOLUTION_CHOICES)
    version = models.IntegerField(null=True, blank=True)

    architect = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True, related_name='solution_design_contact', verbose_name='Architect')
    requester = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True, related_name='solution_requester', verbose_name='Requester')
    
    business_owner_group = models.ForeignKey(Tenant, on_delete=models.SET_NULL, null=True,related_name='solution_business_owner', verbose_name='Business Owner Department')
    business_owner_contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True,related_name='solution_business_owner', verbose_name='Business Owner Contact')
    
    os_technical_contact_group = models.ForeignKey(Tenant, on_delete=models.SET_NULL, null=True,related_name='solution_os_technical_contact', verbose_name='OS Technical Contact Group')  
    os_technical_contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True,related_name='solution_os_technical_contact', verbose_name='OS Technical Contact')
    
    app_technical_contact_group = models.ForeignKey(Tenant, on_delete=models.SET_NULL, null=True,related_name='solution_app_technical_contact', verbose_name='Application Technical Contact Group')
    app_technical_contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True,related_name='solution_app_technical_contact', verbose_name='Application Technical Contact')
    
    incident_contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True,related_name='incident_contact', verbose_name='Incident Contact')

    data_classification = models.CharField(null=True,choices=DATA_CHOICES, verbose_name='Data Classification')
    compliance_requirements = models.CharField(null=True, blank=True, choices=COMPLIANCE_STANDARDS, verbose_name='Compliance Standards')
    fault_tolerence = models.ForeignKey(FaultTolerence, on_delete=models.SET_NULL, null=True, related_name='solutions',verbose_name='Fault Tolerence')
    slos = models.ForeignKey(SLO, on_delete=models.SET_NULL, null=True, related_name='solutions',verbose_name='Service Level Objectives')
    
    last_bcdr_test = models.DateField(null=True, blank=True)
    last_risk_assessment = models.DateField(null=True, blank=True)
    last_review = models.DateField(null=True, blank=True)

    production_readiness_status = models.CharField(max_length=255, null=True, blank=True)
    vendor_management_status = models.CharField(max_length=255, null=True, blank=True)
 
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,  
        default=STATUS_INACTIVE,    
    )
    
    previous_version = models.ForeignKey(
        'self',  # Self-reference to the same model
        on_delete=models.SET_NULL,  # Allow deletion without deleting related records
        null=True,  # Previous version can be optional (i.e., the first version will have no previous_version)
        blank=True,
        related_name='next_versions',  # Allows backward reference from the newer version to older ones
        help_text="Previous version"
    )
    
    class Meta:
        ordering = ['name']
        verbose_name = ('Solution')
        verbose_name_plural = ('Solutions') 
    
    def __str__(self):
        return f'{self.name}'   
    
    def get_absolute_url(self):
        return reverse('plugins:netbox_sm:solution', kwargs={'pk': self.pk})

class Deployment(NetBoxModel):
    
    name = models.CharField(max_length=255)  
    description = models.TextField()
    version = models.IntegerField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,  
        default=STATUS_INACTIVE,    
    )

    deployment_type = models.CharField(max_length=255, choices=DEPLOYMENT_TYPES, verbose_name='Deployment Type')
    deployment_solution = models.ForeignKey(Solution, on_delete=models.SET_NULL, null=True, related_name='deployments', verbose_name="Solution")
    deployment_vlan = models.ForeignKey(VLAN, on_delete=models.SET_NULL, null=True, related_name='deployments', verbose_name="VLAN")
    deployment_prefix = models.ForeignKey(Prefix, on_delete=models.SET_NULL, null=True, related_name='deployments', verbose_name="Prefix")
    deployment_site = models.ForeignKey(Site, on_delete=models.SET_NULL, null=True, related_name='deployments', verbose_name="Site")
    
    # Self-referencing foreign key to track the previous version of the template
    previous_version = models.ForeignKey(
        'self',  # Self-reference to the same model
        on_delete=models.SET_NULL,  # Allow deletion without deleting related records
        null=True,  # Previous version can be optional (i.e., the first version will have no previous_version)
        blank=True,
        related_name='next_versions',  # Allows backward reference from the newer version to older ones
        help_text="Previous version"
    )
    
    class Meta:
        ordering = ['name']
        verbose_name = ('Deployment')
        verbose_name_plural = ('Deployments') 
    
    def __str__(self):
        return f'{self.name}'   
    
    def get_absolute_url(self):
        return reverse('plugins:netbox_sm:deployment', kwargs={'pk': self.pk})

    
class Component(NetBoxModel):
    
    name = models.CharField(max_length=255)
    description = models.TextField()
    version = models.IntegerField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,  
        default=STATUS_INACTIVE,    
    )
    component_deployment = models.ForeignKey(Deployment, on_delete=models.SET_NULL, null=True, related_name='components', verbose_name="Deployment")
    component_prefix = models.ForeignKey(Prefix, on_delete=models.SET_NULL, null=True, related_name='components', verbose_name="Prefix")
    component_vlan = models.ForeignKey(VLAN, on_delete=models.SET_NULL, null=True, related_name='components', verbose_name="VLAN")
    component_site = models.ForeignKey(Site, on_delete=models.SET_NULL, null=True, related_name='components', verbose_name="Site")
    
    # Object type (GenericForeignKey) - allows dynamic references to any object type
    object_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('object_type', 'object_id')
    #vlan / prefix
    #storage type
    #site    
    
    # Self-referencing foreign key to track the previous version of the template
    previous_version = models.ForeignKey(
        'self',  # Self-reference to the same model
        on_delete=models.SET_NULL,  # Allow deletion without deleting related records
        null=True,  # Previous version can be optional (i.e., the first version will have no previous_version)
        blank=True,
        related_name='next_versions',  # Allows backward reference from the newer version to older ones
        help_text="Previous version"
    )
    
    class Meta:
        ordering = ['name']
        verbose_name = ('Component')
        verbose_name_plural = ('Components') 
    
    def __str__(self):
        return f'{self.name}'   
    
    def get_absolute_url(self):
        return reverse('plugins:netbox_sm:component', kwargs={'pk': self.pk})