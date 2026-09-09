from django.shortcuts import render

from main.models import Experience


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
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Fayyad Mohammad Madani",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)