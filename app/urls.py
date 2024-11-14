from django.urls import path
from . views import (HomeView,
                     TaskCreateView,
                     ProjectView,
                     EditProjectView,
                     CreateProjectView,
                     DeleteProjectView,
                     TaskUpdateView,
                     TaskDeleteView,
                     export_to_gist,
                     save_summary)

urlpatterns = [
    path("", HomeView.as_view(template_name="app/home.html"), name="home"),

    # Project Path
    path("project-detail/<int:pk>", ProjectView.as_view(template_name="app/project/projects.html"), name="project-detail"),
    path("edit-project/<int:pk>", EditProjectView.as_view(template_name="app/project/edit_project.html"), name="edit-project"),
    path("create-project/", CreateProjectView.as_view(template_name="app/project/create_project.html"), name="create-project"),
    path("delete-project/<int:pk>", DeleteProjectView.as_view(template_name="app/project/delete_project.html"), name="delete-project"),

    # Task Path
    path("create-task/<int:pk>", TaskCreateView.as_view(template_name="app/task/create_task.html"), name="create-task"),
    path("update-task/<int:pk>", TaskUpdateView.as_view(template_name="app/task/update_task.html"), name="update-task"),
    path("delete-task/<int:pk>", TaskDeleteView.as_view(template_name="app/task/delete_task.html"), name="delete-task"),
    path("export-to-gist/<int:pk>", export_to_gist, name="export-to-gist"),
    path("save-summary/<int:pk>", save_summary, name="save-summary")
]