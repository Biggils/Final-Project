from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Q
from django.utils import timezone

from .models import Task, Project
from .serializers import TaskSerializer, ProjectSerializer
from .permissions import ProjectPermission, TaskPermission


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    filterset_fields = ['status', 'project', 'assigned_to']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'due_date', 'title']
    ordering = ['-created_at']

    permission_classes = [IsAuthenticated,TaskPermission]

    def get_queryset(self):
        return Task.objects.filter(
            Q(project__owner=self.request.user) |
            Q(project__members=self.request.user)
        ).select_related('project', 'assigned_to').distinct()

    @action(detail=False, methods=['get'])
    def overdue(self, request):
        overdue_tasks = self.get_queryset().filter(
            due_date__lt=timezone.localdate()
        ).exclude(status='Completed')

        serializer = self.get_serializer(overdue_tasks, many=True)
        return Response(serializer.data)


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'name']
    ordering = ['-created_at']
    permission_classes = [ProjectPermission]

    def get_queryset(self):
        return Project.objects.filter(
            Q(owner=self.request.user) |
            Q(members=self.request.user)
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=False, methods=['get'])
    def task_summary(self, request):
        projects = self.get_queryset().annotate(
            total_tasks=Count('tasks'),
            completed_tasks=Count(
                'tasks',
                filter=Q(tasks__status='Completed')
            )
        )

        results = projects.values(
            'id',
            'name',
            'total_tasks',
            'completed_tasks'
        )

        return Response(results)