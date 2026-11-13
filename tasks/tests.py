from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Project, Task


class ProjectModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123'
        )

    def test_project_creation(self):
        project = Project.objects.create(
            name='Test Project',
            description='A project for testing',
            owner=self.user
        )

        self.assertEqual(project.name, 'Test Project')
        self.assertEqual(project.owner, self.user)


class TaskAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123'
        )

        self.project = Project.objects.create(
            name='Test Project',
            owner=self.user
        )

    def test_create_task(self):
        data = {
            'title': 'Test Task',
            'description': 'Testing task creation',
            'project': self.project.id,
            'assigned_to': self.user.id,
            'status': 'Pending'
        }

        response = self.client.post(
            '/api/tasks/',
            data,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_empty_task_title_is_rejected(self):
        data = {
            'title': '',
            'description': 'Invalid task',
            'project': self.project.id,
            'status': 'Pending'
        }

        response = self.client.post(
            '/api/tasks/',
            data,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
