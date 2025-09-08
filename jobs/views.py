from rest_framework import viewsets
from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated
from .models import Job, JobTask
from .serializers import JobSerializer, JobTaskSerializer
from authentication.permissions import IsAdminOrSalesAgent, IsAssignedTechnician
from equipment.models import Equipment
from django.db.models import Avg, Count
from rest_framework.response import Response
from authentication.permissions import IsAdmin
from django.db.models import Avg, F, ExpressionWrapper, DurationField

from logs.models import AuditLog
from rest_framework.exceptions import ValidationError

from .filters import JobFilter

# class JobViewSet(viewsets.ModelViewSet):
#     queryset = Job.objects.all()
#     serializer_class = JobSerializer
#     permission_classes = [IsAuthenticated & IsAdminOrSalesAgent]

# class JobTaskViewSet(viewsets.ModelViewSet):
#     queryset = JobTask.objects.all()
#     serializer_class = JobTaskSerializer
#     permission_classes = [IsAuthenticated & IsAssignedTechnician]


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated & IsAdminOrSalesAgent]
    # filterset_fields = ['status', 'priority', 'assigned_to', 'created_by', 'scheduled_date']
    filterset_class = JobFilter

    def perform_create(self, serializer):
        job = serializer.save(created_by=self.request.user)
        AuditLog.objects.create(user=self.request.user, job=job, action='created')

    def perform_update(self, serializer):
        job_instance = self.get_object()
        new_status = serializer.validated_data.get('status', job_instance.status)

        if new_status == 'Completed':
            incomplete_tasks = job_instance.tasks.exclude(status='Completed').exists()
            if incomplete_tasks:
                raise ValidationError(
                    {"status": "Cannot mark job as Completed until all tasks are completed."}
                )
        job = serializer.save()
        try:
            AuditLog.objects.create(user=self.request.user, job=job, action='updated', changes=self.request.data)
        except Exception as es:
            print("JobViewSet perform_update_error  in AuditLog",es)

class JobTaskViewSet(viewsets.ModelViewSet):
    queryset            = JobTask.objects.select_related('job').all()
    serializer_class    = JobTaskSerializer
    permission_classes  = [IsAuthenticated & IsAssignedTechnician]
    filterset_fields = ['status', 'job', 'order']  

    def perform_create(self, serializer):
        task = serializer.save()
        try:
            AuditLog.objects.create(user=self.request.user, task=task, action='created')
        except Exception as es:
            print("JobTaskViewSet perform_create_error in AuditLog")

    def perform_update(self, serializer):
        task = serializer.save()
        try:
            AuditLog.objects.create(user=self.request.user,task=task, action='updated', changes=self.request.data)
        except Exception as es:
            print("JobTaskViewSet sperform_update_error in AuditLog")

class JobAnalyticsView(APIView):
    permission_classes = [IsAuthenticated & IsAdmin]

    def get(self, request):
        # Average completion time
        avg_task_time = JobTask.objects.exclude(completed_at__isnull=True).annotate(
            duration=ExpressionWrapper(
                F('completed_at') - F('job__scheduled_date'),
                output_field=DurationField()
            )
        ).aggregate(average_duration=Avg('duration'))['average_duration']

        # Most used equipment
        equipment_counts = Equipment.objects.annotate(
            task_count=Count('jobtask')
        ).order_by('-task_count')[:5]

        most_used_equipment = [
            {"equipment": e.name, "used_in_tasks": e.task_count}
            for e in equipment_counts
        ]

        return Response({
            "average_task_time": avg_task_time,
            "most_used_equipment": most_used_equipment
        })