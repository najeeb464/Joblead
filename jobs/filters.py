import django_filters
from .models import Job

class JobFilter(django_filters.FilterSet):
    min_date = django_filters.DateFilter(field_name='scheduled_date', lookup_expr='gte')
    max_date = django_filters.DateFilter(field_name='scheduled_date', lookup_expr='lte')

    class Meta:
        model = Job
        fields = ['status', 'priority', 'assigned_to', 'min_date', 'max_date']