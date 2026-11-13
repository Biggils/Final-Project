from rest_framework import serializers
from .models import Task, Project


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'project',
            'assigned_to',
            'status',
            'due_date',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                "Task title cannot be empty."
            )
        return value

    def validate_status(self, value):
        valid_statuses = [
            choice[0] for choice in Task.STATUS_CHOICES
        ]

        if value not in valid_statuses:
            raise serializers.ValidationError(
                "Invalid task status."
            )
        return value


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'owner']

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                "Project name cannot be empty."
            )
        return value
    