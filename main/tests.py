from django.contrib.auth.models import AnonymousUser, Group, User
from django.test import TestCase
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone

from main.models import Experience, Project
from main.permissions import (
    EDITOR_GROUP_NAME,
    can_create_or_delete,
    can_edit,
    is_editor,
)


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)


class ExperienceTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
        )

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Part-Time")
        self.assertContains(response, "Sedang berlangsung")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, "Selesai")
        self.assertNotContains(response, "Sedang berlangsung")


class ProjectTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            title="Portfolio Website",
            description="Situs portofolio pribadi dibangun dengan Django.",
            thumbnail="https://example.com/project-1.webp",
        )

    def test_projects_url_is_accessible(self):
        response = self.client.get(reverse("main:show_projects"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects.html")

    def test_project_page_shows_data(self):
        response = self.client.get(reverse("main:show_projects"))

        self.assertContains(response, self.project.title)
        self.assertContains(response, self.project.description)

    def test_empty_projects_page(self):
        Project.objects.all().delete()
        response = self.client.get(reverse("main:show_projects"))

        self.assertContains(response, "Belum ada proyek yang ditambahkan.")


class PermissionHelperTest(TestCase):
    """Menguji helper otorisasi untuk keempat peran pengguna."""

    def setUp(self):
        self.anonymous = AnonymousUser()
        self.regular = User.objects.create_user(
            username="pengguna", password="rahasia123"
        )
        self.editor = User.objects.create_user(
            username="editor", password="rahasia123"
        )
        self.editor.groups.add(Group.objects.get(name=EDITOR_GROUP_NAME))
        self.owner = User.objects.create_superuser(
            username="pemilik", password="rahasia123"
        )

    def test_editor_group_is_created_by_migration(self):
        self.assertTrue(Group.objects.filter(name=EDITOR_GROUP_NAME).exists())

    def test_only_group_member_is_recognized_as_editor(self):
        self.assertFalse(is_editor(self.anonymous))
        self.assertFalse(is_editor(self.regular))
        self.assertTrue(is_editor(self.editor))
        self.assertFalse(is_editor(self.owner))

    def test_edit_is_allowed_for_editor_and_owner(self):
        self.assertFalse(can_edit(self.anonymous))
        self.assertFalse(can_edit(self.regular))
        self.assertTrue(can_edit(self.editor))
        self.assertTrue(can_edit(self.owner))

    def test_create_and_delete_are_limited_to_owner(self):
        self.assertFalse(can_create_or_delete(self.anonymous))
        self.assertFalse(can_create_or_delete(self.regular))
        self.assertFalse(can_create_or_delete(self.editor))
        self.assertTrue(can_create_or_delete(self.owner))


class ForbiddenPageTest(TestCase):
    """Memastikan template 403 dapat dirender tanpa error."""

    def test_403_template_renders(self):
        html = render_to_string("403.html")
        self.assertIn("403", html)
        self.assertIn("Forbidden", html)
