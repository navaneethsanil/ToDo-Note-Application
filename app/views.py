from typing import Any
from django.db.models.query import QuerySet
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.forms import BaseModelForm
from django.views.generic import (ListView,
                                  CreateView,
                                  UpdateView,
                                  DetailView,
                                  DeleteView)
from . models import Task, Project
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.contrib import messages
from . utils import export_all_projects_to_gist_and_local

class HomeView(LoginRequiredMixin, ListView):
    model = Project
    context_object_name = "projects"

    # Only fetches current user project
    def get_queryset(self) -> QuerySet[Any]:
        user_projects = Project.objects.filter(createdBy=self.request.user)
        return user_projects


class CreateProjectView(LoginRequiredMixin, CreateView):
    model = Project
    fields = ["title"]
    success_url = "/"

    def form_valid(self, form: BaseModelForm):
        form.instance.createdBy = self.request.user
        messages.success(self.request, "Project created successfully!")
        return super().form_valid(form)
    

class ProjectView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = "tasks"

    def get_queryset(self):
        project_id = self.kwargs.get("pk")
        project = get_object_or_404(Project, id=project_id)
        
        # Return only Tasks associated with this project
        return Task.objects.filter(project=project)
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.kwargs.get("pk")
        project = get_object_or_404(Project, id=project_id)
        # Add the project title to the context
        context['project_id'] = project_id
        context['project_title'] = project.title
        
        return context


class EditProjectView(LoginRequiredMixin, UpdateView):
    model = Project
    fields = ["title"]

    
    def form_valid(self, form):
        messages.success(self.request, "Project title updated successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("project-detail", kwargs={"pk": self.object.pk})
    


class DeleteProjectView(LoginRequiredMixin, DeleteView):
    model = Project
    success_url = "/"

    def get_success_url(self) -> str:
        messages.success(self.request, "Project deleted successfully!")
        return super().get_success_url()


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ["description", "status"]

    def form_valid(self, form: BaseModelForm):
        # Get the project from the URL parameter
        project_id = self.kwargs.get('pk')
        project = Project.objects.get(id=project_id)
        
        # Set the 'project' field and other data
        form.instance.project = project

        messages.success(self.request, "New task created")
        
        return super().form_valid(form)
    
    

    def get_success_url(self):
        return reverse("project-detail", kwargs={"pk": self.object.project.pk})



class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    fields = ["description", "status"]

    def test_func(self):
        task = self.get_object()
        if self.request.user == task.project.createdBy:
            return True
        else:
            return False
    
    def form_valid(self, form):
        messages.success(self.request, "Task updated successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("project-detail", kwargs={"pk": self.object.project.pk})
    



class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    success_url = "/"

    def test_func(self):
        task = self.get_object()
        if self.request.user == task.project.createdBy:
            return True
        else:
            return False
        
    def form_valid(self, form):
        messages.success(self.request, "Task deleted successfully!")
        return super().form_valid(form)
    

    def get_success_url(self):
        return reverse("project-detail", kwargs={"pk": self.object.project.pk})
    








def export_to_gist(request, pk):
    gist_url = export_all_projects_to_gist_and_local(pk)
    messages.success(request, "Project summary has been successfully saved both locally and to GitHub Gist.")
    return redirect(reverse("project-detail", kwargs={"pk": pk}))

