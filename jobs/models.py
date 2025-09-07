from django.db import models

# Create your models here.
from django.db import models
from authentication.models import User
from equipment.models import Equipment

class Job(models.Model):
    STATUS_CHOICES = [('Pending','Pending'),('InProgress','InProgress'),('Completed','Completed')]
    PRIORITY_CHOICES = [('Low','Low'),('Medium','Medium'),('High','High')]
    
    title           = models.CharField(max_length=255)
    description     = models.TextField()
    client_name     = models.CharField(max_length=255)
    created_by      = models.ForeignKey(User, related_name='created_jobs', on_delete=models.SET_NULL, null=True)
    assigned_to     = models.ForeignKey(User, related_name='assigned_jobs', on_delete=models.SET_NULL, null=True)
    status          = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    priority        = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Medium')
    scheduled_date  = models.DateField()
    overdue         = models.BooleanField(default=False)

class JobTask(models.Model):
    STATUS_CHOICES = [('Pending','Pending'),('InProgress','InProgress'),('Completed','Completed')]
    
    job                 = models.ForeignKey(Job, related_name='tasks', on_delete=models.CASCADE)
    title               = models.CharField(max_length=255)
    description         = models.TextField()
    status              = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    required_equipment  = models.ManyToManyField(Equipment, blank=True)
    completed_at        = models.DateTimeField(null=True, blank=True)
    order               = models.PositiveIntegerField()
