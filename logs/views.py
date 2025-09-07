
from rest_framework.views import APIView
from rest_framework import viewsets

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from jobs.models import JobTask

from .models import AuditLog
from .serializers import AuditLogSerializer
from authentication.permissions import IsAdmin

class TechnicianDashboard(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = JobTask.objects.filter(job__assigned_to=request.user, status__in=['Pending','InProgress'])
        data = {}
        for task in tasks:
            date = task.job.scheduled_date
            if date not in data:
                data[date] = []
            data[date].append({
                'job_title': task.job.title,
                'task_title': task.title,
                'task_status': task.status,
                'equipment': list(task.required_equipment.values('name','serial_number'))
            })
        return Response(data)




class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.all().order_by('-timestamp')
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated & IsAdmin]