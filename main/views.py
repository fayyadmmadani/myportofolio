from django.db.models import F
from django.shortcuts import render

from django.conf import settings
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from main.models import Experience, Project
from main.forms import ProjectForm


def show_main(request):
    context = {
        "name": "Fayyad Mohammad Madani",
        "npm": "2506622720",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            """An Information Systems student who enjoys building digital products
          that are clean and genuinely useful. Guided by integrity,
          collaboration, and critical thinking — always curious, from interface
          design to web development."""
        ),
        "experience_list": Experience.objects.all().order_by(
            F("ended_at").desc(nulls_first=True), "-started_at"
        )[:2],
        "project_list": Project.objects.all().order_by("-order", "-created_at")[:2],
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Fayyad Mohammad Madani",
        "experience_list": Experience.objects.all().order_by(
            F("ended_at").desc(nulls_first=True), "-started_at"
        ),
    }
    return render(request, "experience.html", context)


def show_projects(request):
    json_response = get_projects_json(request)

    projects = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    projects = [project.object for project in projects]
    title_query = request.GET.get("title", "").strip()
    
    context = {
        "name": "Fayyad Mohammad Madani",
        "project_list": projects,
        "title_query": title_query,
    }
    return render(request, "projects.html", context)

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize("json", projects)
    return HttpResponse(projects_json, content_type="application/json")

def create_project(request):
    form = ProjectForm(request.POST or None)

    if request.method == "POST":
        if request.POST.get("secret") != settings.EDIT_SECRET:
            messages.error(request, "Password salah!")
            return redirect("main:show_projects")
        if form.is_valid():
            form.save()
            messages.success(request, "Proyek baru berhasil ditambahkan!")
            return redirect("main:show_projects")

    context = {
        "name": "Fayyad Mohammad Madani",
        "form": form,
    }
    return render(request, "projects_form.html", context)

def edit_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    form = ProjectForm(request.POST or None, instance=project)

    if request.method == "POST":
        if request.POST.get("secret") != settings.EDIT_SECRET:
            messages.error(request, "Password salah!")
            return redirect("main:show_projects")
        if form.is_valid():
            form.save()
            messages.success(request, "Proyek berhasil diperbarui!")
            return redirect("main:show_projects")

    context = {
        "name": "Fayyad Mohammad Madani",
        "form": form,
    }
    return render(request, "projects_form.html", context)

def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        if request.POST.get("secret") != settings.EDIT_SECRET:
            messages.error(request, "Password salah!")
            return redirect("main:show_projects")
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_projects")

    return redirect("main:show_projects")