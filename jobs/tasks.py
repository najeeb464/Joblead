from celery import shared_task
from .models import Job
from django.utils import timezone

@shared_task
def update_overdue_jobs():
    today = timezone.now().date()
    Job.objects.filter(scheduled_date__lt=today, status__in=['Pending','InProgress']).update(overdue=True)