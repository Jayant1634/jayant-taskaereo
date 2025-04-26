"""
URL configuration for web_django project.
"""
from django.contrib import admin
from django.urls import path, include
from tasks.views import TaskListView

urlpatterns = [
    path('', TaskListView.as_view(), name='task-list'),
    path('admin/', admin.site.urls),
    path('api/tasks/', include('tasks.urls')),  # Changed to explicitly include tasks URLs
]
