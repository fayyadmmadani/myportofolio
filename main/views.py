from django.db.models import F
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
        "experience_list": Experience.objects.all().order_by(
            F("ended_at").desc(nulls_first=True), "-started_at"
        )[:2],
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