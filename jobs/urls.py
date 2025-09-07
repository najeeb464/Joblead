from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobViewSet, JobTaskViewSet
from .views import JobAnalyticsView
router = DefaultRouter()
router.register('jobs', JobViewSet)
router.register('tasks', JobTaskViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('analytics/', JobAnalyticsView.as_view(), name='job-analytics'),
]
