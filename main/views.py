from django.db.models import F
from django.shortcuts import render

from main.models import Experience, Project
from main.forms import ProjectForm, ExperienceForm


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
    json_response = get_experience_json(request)

    experiences = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    experiences = [experience.object for experience in experiences]

    context = {
        "name": "Fayyad Mohammad Madani",
        "experience_list": experiences,
    }
    return render(request, "experience.html", context)

def get_experience_json(request):
    category_query = request.GET.get("category", "").strip()
    experiences = Experience.objects.all().order_by(
        F("ended_at").desc(nulls_first=True), "-started_at"
    )
    
    if category_query:
        experiences = experiences.filter(category=category_query)
    
    experience_json = serializers.serialize("json", experiences)
    return HttpResponse(experience_json, content_type="application/json")

def create_experience(request):
    form = ExperienceForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Experience baru berhasil ditambahkan!")
        return redirect("main:show_experience")

    context = {
        "name": "Fayyad Mohammad Madani",
        "form": form,
    }
    return render(request, "experience_form.html", context)

def edit_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)
    form = ExperienceForm(request.POST or None, instance=experience)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Experience berhasil diperbarui!")
        return redirect("main:show_experience")

    context = {
        "name": "Fayyad Mohammad Madani",
        "form": form,
    }
    return render(request, "experience_form.html", context)

def delete_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        experience.delete()
        messages.success(request, "Experience berhasil dihapus!")
        return redirect("main:show_experience")

    return redirect("main:show_experience")

def show_projects(request):
    context = {
        "name": "Fayyad Mohammad Madani",
        "project_list": Project.objects.all().order_by("-order", "-created_at"),
    }
    return render(request, "projects.html", context)