from django.db import models
from django.contrib.auth import get_user_model
from jobs.models import Job, JobTask

User = get_user_model()

class AuditLog(models.Model):
    ACTION_CHOICES = (
        ('created','Created'),
        ('updated','Updated'),
        ('deleted','Deleted'),
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, null=True, blank=True)
    task = models.ForeignKey(JobTask, on_delete=models.CASCADE, null=True, blank=True)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    changes = models.JSONField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
