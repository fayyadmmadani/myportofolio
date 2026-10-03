from django.db.models import F
import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.exceptions import PermissionDenied  
from django.http import HttpResponse, JsonResponse
from django.utils import timezone, translation
from django.utils.formats import date_format
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from main.models import Experience, Project
from main.forms import ProjectForm, ExperienceForm
from main.permissions import can_create_or_delete, can_edit, is_editor

def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "Fayyad Mohammad Madani",
        "form": form,
    }
    return render(request, "register.html", context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "name": "Fayyad Mohammad Madani",
        "form": form,
    }
    return render(request, "login.html", context)

def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response

def show_main(request):
    last_login = request.COOKIES.get('last_login', 'Belum ada sesi login / Cookie tidak ditemukan')
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
        "last_login": last_login,
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Fayyad Mohammad Madani",
        "form": ExperienceForm(),
        "categories": Experience.EXPERIENCE_CHOICES,
        "is_editor": is_editor(request.user),
    }
    return render(request, "experience.html", context)

def _format_experience_period(experience):
    """Format rentang waktu experience (locale Indonesia) untuk respons JSON."""
    with translation.override("id"):
        started = date_format(timezone.localtime(experience.started_at), "j M Y")
        if experience.ended_at is None:
            return f"{started} - sekarang"
        ended = date_format(timezone.localtime(experience.ended_at), "j M Y")
        return f"{started} - {ended}"

def get_experience_json(request):
    category_query = request.GET.get("category", "").strip()
    title_query = request.GET.get("title", "").strip()
    experiences = Experience.objects.all().order_by(
        F("ended_at").desc(nulls_first=True), "-started_at"
    )

    if category_query:
        experiences = experiences.filter(category=category_query)
    if title_query:
        experiences = experiences.filter(title__icontains=title_query)

    # Konstruksi data JSON secara manual (hanya field yang dibutuhkan tampilan)
    data = [
        {
            "pk": str(experience.id),
            "fields": {
                "title": experience.title,
                "description": experience.description,
                "category": experience.category,
                "category_display": experience.get_category_display(),
                "thumbnail": experience.thumbnail or "",
                "is_ongoing": experience.is_ongoing,
                "period": _format_experience_period(experience),
            },
        }
        for experience in experiences
    ]
    return JsonResponse(data, safe=False)

@login_required(login_url="/login/")
def create_experience(request):
    # Authorization: hanya pemilik portofolio yang boleh menambah data
    if not can_create_or_delete(request.user):
        raise PermissionDenied
    
    form = ExperienceForm(request.POST or None)

    if request.method == "POST":
        if request.POST.get("secret") != settings.EDIT_SECRET:
            messages.error(request, "Password salah!")
            return redirect("main:show_experience")
        if form.is_valid():
            form.save()
            messages.success(request, "Experience baru berhasil ditambahkan!")
            return redirect("main:show_experience")

    context = {
        "name": "Fayyad Mohammad Madani",
        "form": form,
    }
    return render(request, "experience_form.html", context)

@require_POST
def create_experience_ajax(request):
    # Authorization di sisi server: hanya pemilik portofolio (bukan sekadar
    # menyembunyikan tombol di template). @login_required tidak dipakai agar
    # pengunjung mendapat JSON 403, bukan redirect ke halaman login.
    if not can_create_or_delete(request.user):
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan experience."},
            status=403,
        )

    if request.POST.get("secret") != settings.EDIT_SECRET:
        return JsonResponse({"message": "Password salah!"}, status=403)

    form = ExperienceForm(request.POST)
    if form.is_valid():
        experience = form.save()
        return JsonResponse(
            {"message": "Experience berhasil ditambahkan.", "pk": str(experience.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)

@login_required(login_url="/login/")
def edit_experience(request, experience_id):
    # Authorization: pemilik portofolio dan Editor boleh mengubah data
    if not can_edit(request.user):
        raise PermissionDenied
    
    experience = get_object_or_404(Experience, pk=experience_id)
    form = ExperienceForm(request.POST or None, instance=experience)

    if request.method == "POST":
        if request.POST.get("secret") != settings.EDIT_SECRET:
            messages.error(request, "Password salah!")
            return redirect("main:show_experience")
        if form.is_valid():
            form.save()
            messages.success(request, "Experience berhasil diperbarui!")
            return redirect("main:show_experience")

    context = {
        "name": "Fayyad Mohammad Madani",
        "form": form,
    }
    return render(request, "experience_form.html", context)

@login_required(login_url="/login/")
def delete_experience(request, experience_id):
    # Authorization: hanya pemilik portofolio yang boleh menghapus data
    if not can_create_or_delete(request.user):
        raise PermissionDenied
    
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        if request.POST.get("secret") != settings.EDIT_SECRET:
            messages.error(request, "Password salah!")
            return redirect("main:show_experience")
        experience.delete()
        messages.success(request, "Experience berhasil dihapus!")
        return redirect("main:show_experience")

    return redirect("main:show_experience")

def show_projects(request):
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Fayyad Mohammad Madani",
        "title_query": title_query,
        "form": ProjectForm(),
        "is_editor": is_editor(request.user),
    }
    return render(request, "projects.html", context)

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.prefetch_related("starred_by").all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    # Konstruksi data JSON secara manual agar bisa menyisipkan logika Star
    data = []
    for project in projects:
        starred_users = project.starred_by.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else False
        starred_by_names = ", ".join([u.username for u in starred_users])

        data.append({
            "pk": str(project.id),
            "fields": {
                "title": project.title,
                "description": project.description,
                "thumbnail": project.thumbnail,
                "order": project.order,
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            }
        })

    return JsonResponse(data, safe=False)

@login_required(login_url="/login/")
def create_project(request):
    # Authorization: hanya pemilik portofolio yang boleh menambah data
    if not can_create_or_delete(request.user):
        raise PermissionDenied

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

@require_POST
def create_project_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan proyek."},
            status=403,
        )

    form = ProjectForm(request.POST)
    if form.is_valid():
        project = form.save()
        return JsonResponse(
            {"message": "Proyek berhasil ditambahkan.", "pk": str(project.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)

@login_required(login_url="/login/")
def edit_project(request, project_id):
    # Authorization: pemilik portofolio dan Editor boleh mengubah data
    if not can_edit(request.user):
        raise PermissionDenied
    
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

@login_required(login_url="/login/")
def toggle_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        # Kalau akun ini sudah pernah memberi star, batalkan star-nya.
        # Kalau belum, tambahkan star.
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)

    return redirect("main:show_projects")

@login_required(login_url="/login/")
def delete_project(request, project_id):
    # Authorization: hanya pemilik portofolio yang boleh menghapus data
    if not can_create_or_delete(request.user):
        raise PermissionDenied
    
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        if request.POST.get("secret") != settings.EDIT_SECRET:
            messages.error(request, "Password salah!")
            return redirect("main:show_projects")
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_projects")

    return redirect("main:show_projects")