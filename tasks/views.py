from rest_framework import viewsets, status
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.parsers import JSONParser
from django_filters.rest_framework import DjangoFilterBackend
from django.views.generic import ListView
from django.shortcuts import render
from .models import Task
from .serializers import TaskSerializer
from django.utils import timezone
import logging
from django.core.cache import cache
import hashlib
import json
import time

# Set up logging
logger = logging.getLogger(__name__)

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['created_date']
    filterset_fields = {
        'created_date': ['exact', 'gte', 'lte']
    }

    def create(self, request, *args, **kwargs):
        try:
            # Log the request information
            submission_id = request.headers.get('X-Submission-ID', 'unknown')
            request_id = request.headers.get('X-Request-ID', 'unknown')
            logger.info(f"Task create request received - Submission ID: {submission_id}, Request ID: {request_id}")
            logger.info(f"Request data: {request.data}")
            
            # Check if this is a potential duplicate submission within a short time window
            title = request.data.get('title', '')
            description = request.data.get('description', '')
            
            # Create a hash of the task data to use as a lock key
            task_data_hash = hashlib.md5(
                json.dumps({'title': title, 'description': description}, sort_keys=True).encode()
            ).hexdigest()
            lock_key = f"task_create_lock_{task_data_hash}"
            
            # First, check if a task was recently created with this data
            recent_identical_task = Task.objects.filter(
                title=title,
                description=description,
                created_date__gte=timezone.now() - timezone.timedelta(seconds=30)
            ).first()
            
            if recent_identical_task:
                logger.warning(f"Immediate duplicate detected - Task already exists - ID: {recent_identical_task.id}, Request ID: {request_id}")
                serializer = self.get_serializer(recent_identical_task)
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            # Try to acquire a lock - returns False if the lock already exists
            lock_acquired = cache.add(lock_key, request_id, timeout=30)  # 30 second lock timeout
            
            if not lock_acquired:
                current_lock_holder = cache.get(lock_key)
                logger.warning(f"Lock acquisition failed - Current lock holder: {current_lock_holder}, Request ID: {request_id}")
                
                # Wait briefly to see if a task has been created in the meantime
                time.sleep(0.5)
                
                # Check again for recently created task
                recent_identical_task = Task.objects.filter(
                    title=title,
                    description=description,
                    created_date__gte=timezone.now() - timezone.timedelta(seconds=30)
                ).first()
                
                if recent_identical_task:
                    logger.warning(f"Duplicate task found after lock check - ID: {recent_identical_task.id}, Request ID: {request_id}")
                    serializer = self.get_serializer(recent_identical_task)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    # If no existing task found but lock exists, return a clear error
                    logger.warning(f"Returning 429 - Another task creation in progress - Request ID: {request_id}")
                    return Response(
                        {'detail': 'Another task creation is in progress'},
                        status=status.HTTP_429_TOO_MANY_REQUESTS
                    )
            
            try:
                logger.info(f"Lock acquired - Creating task - Request ID: {request_id}")
                serializer = self.get_serializer(data=request.data)
                if serializer.is_valid():
                    self.perform_create(serializer)
                    headers = self.get_success_headers(serializer.data)
                    task_id = serializer.data.get('id')
                    logger.info(f"Task created successfully - ID: {task_id}, Request ID: {request_id}")
                    return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
                
                logger.error(f"Serializer validation failed - Request ID: {request_id}, Errors: {serializer.errors}")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            finally:
                # Always release the lock when done
                logger.info(f"Releasing lock - Request ID: {request_id}")
                cache.delete(lock_key)
        except Exception as e:
            logger.exception(f"Error creating task - Request ID: {request_id if 'request_id' in locals() else 'unknown'}, Error: {str(e)}")
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        queryset = Task.objects.all()
        sort_by_date = self.request.query_params.get('sort_by_date', None)
        search_date = self.request.query_params.get('search_date', None)
        
        if sort_by_date == 'true':
            queryset = queryset.order_by('-created_date')
        elif sort_by_date == 'false':
            queryset = queryset.order_by('created_date')
        if search_date:
            queryset = queryset.filter(created_date__date=search_date)
            
        return queryset

class TaskListView(ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    ordering = ['-created_date']

    def get_queryset(self):
        queryset = Task.objects.all()
        search = self.request.GET.get('search')
        search_date = self.request.GET.get('search_date')
        sort_by_date = self.request.GET.get('sort_by_date')

        if search:
            queryset = queryset.filter(title__icontains=search)
        if search_date:
            queryset = queryset.filter(created_date__date=search_date)
        if sort_by_date == 'true':
            queryset = queryset.order_by('-created_date')
        elif sort_by_date == 'false':
            queryset = queryset.order_by('created_date')
        
        return queryset
