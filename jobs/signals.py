from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Job

@receiver(pre_save, sender=Job)
def check_job_completion(sender, instance, **kwargs):
    if instance.status == 'Completed' and instance.tasks.exclude(status='Completed').exists():
        raise ValueError("Cannot complete job until all tasks are completed")


from django_celery_beat.models import PeriodicTask, IntervalSchedule

def create_periodic_tasks(sender, **kwargs):
    schedule, _ = IntervalSchedule.objects.get_or_create(
        every=1,
        period=IntervalSchedule.DAYS,
    )
    PeriodicTask.objects.update_or_create(
        name='Update Overdue Jobs',
        defaults={'interval': schedule, 'task': 'jobs.tasks.update_overdue_jobs'},
    )
