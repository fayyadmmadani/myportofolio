from django.shortcuts import render

from main.models import Experience, Project


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
        "project_list": Project.objects.all().order_by("-order", "-created_at")[:2],
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Fayyad Mohammad Madani",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)


def show_projects(request):
    context = {
        "name": "Fayyad Mohammad Madani",
        "project_list": Project.objects.all().order_by("-order", "-created_at"),
    }
    return render(request, "projects.html", context)