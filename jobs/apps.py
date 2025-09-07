from django.apps import AppConfig


class JobsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'jobs'

    def ready(self):
        from django.db.models.signals import post_migrate
        from .signals import create_periodic_tasks
        post_migrate.connect(create_periodic_tasks, sender=self)
