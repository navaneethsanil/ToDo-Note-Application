from django.test import TestCase
from django.contrib.auth.models import User
from .models import Project, Task

class ProjectModelTest(TestCase):

    def setUp(self):
        # Set up a user and a project for testing
        self.user = User.objects.create_user(username="testuser", password="password")
        self.project = Project.objects.create(
            title="Test Project",
            createdBy=self.user
        )

    def test_project_creation(self):
        # Check if the project was created correctly
        project = Project.objects.get(title="Test Project")
        self.assertEqual(project.title, "Test Project")
        self.assertEqual(project.createdBy, self.user)
        self.assertIsNotNone(project.created_date)

    def test_project_str_method(self):
        # Test the __str__ method of Project
        project = Project.objects.get(title="Test Project")
        self.assertEqual(str(project), "Test Project")

    def test_task_creation(self):
        # Create a Task and verify its fields and relationship with Project
        task = Task.objects.create(
            project=self.project,
            description="Test Task",
            status="Pending"
        )
        self.assertEqual(task.description, "Test Task")
        self.assertEqual(task.status, "Pending")
        self.assertEqual(task.project, self.project)
        self.assertIsNotNone(task.created_date)
        self.assertIsNotNone(task.updated_date)

    def test_task_str_method(self):
        # Test the __str__ method of Task
        task = Task.objects.create(
            project=self.project,
            description="Another Task"
        )
        self.assertEqual(str(task), "Another Task")

    def test_task_default_status(self):
        # Ensure the default status is 'Pending'
        task = Task.objects.create(
            project=self.project,
            description="Task with default status"
        )
        self.assertEqual(task.status, "Pending")

    def test_task_status_choices(self):
        # Ensure that status choices work as expected
        task = Task.objects.create(
            project=self.project,
            description="Completed Task",
            status="Completed"
        )
        self.assertEqual(task.status, "Completed")
    
    def test_get_absolute_url(self):
        # Test the get_absolute_url method for Task
        task = Task.objects.create(
            project=self.project,
            description="Test Task with URL"
        )
        self.assertEqual(task.get_absolute_url(), "/")  # Update this path if 'home' URL differs
