from django.urls import path,include
from .views import TechnicianDashboard
from rest_framework.routers import DefaultRouter
from .views import AuditLogViewSet

router = DefaultRouter()
router.register('audit-logs', AuditLogViewSet)
urlpatterns = [
    path('technician-dashboard/', TechnicianDashboard.as_view()),
    path('', include(router.urls))
]