
from django.db import models
class Equipment(models.Model):
    name = models.CharField(max_length=255)
    _type = models.CharField(max_length=255)
    serial_number = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.serial_number})"
