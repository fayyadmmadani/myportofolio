from django.urls import path

from main.views import show_main, show_experience, show_projects, create_project, get_projects_json, edit_project, delete_project

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("projects/", show_projects, name="show_projects"),
    path("api/projects/", get_projects_json, name="get_projects_json"),
    path("projects/add/", create_project, name="create_project"),
    path("projects/<uuid:project_id>/edit/", edit_project, name="edit_project"),
    path("projects/<uuid:project_id>/delete/", delete_project, name="delete_project"),
]