from django.contrib.auth.models import AnonymousUser, Group, User
from django.test import TestCase, override_settings
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
        self.experience.started_at = timezone.now().replace(
            year=2025, month=1, day=5, hour=12, minute=0, second=0, microsecond=0
        )
        self.experience.ended_at = self.experience.started_at.replace(month=3, day=20)
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, "5 Jan 2025 - 20 Mar 2025")
        self.assertNotContains(response, "Sedang berlangsung")


@override_settings(EDIT_SECRET="rahasia-uji")
class ExperienceAccessTest(TestCase):
    """Menguji hak akses keempat peran pada fitur Experience."""

    SECRET = "rahasia-uji"

    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
        )
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

        self.list_url = reverse("main:show_experience")
        self.create_url = reverse("main:create_experience")
        self.edit_url = reverse("main:edit_experience", args=[self.experience.id])
        self.delete_url = reverse("main:delete_experience", args=[self.experience.id])

    def assertExperienceStillExists(self):
        self.assertTrue(Experience.objects.filter(pk=self.experience.pk).exists())

    def test_anonymous_can_read_but_must_login_to_change(self):
        self.assertEqual(self.client.get(self.list_url).status_code, 200)

        for url in (self.create_url, self.edit_url):
            response = self.client.get(url)
            self.assertRedirects(
                response, f"/login/?next={url}", fetch_redirect_response=False
            )

        response = self.client.post(self.delete_url, {"secret": self.SECRET})
        self.assertRedirects(
            response, f"/login/?next={self.delete_url}", fetch_redirect_response=False
        )
        self.assertExperienceStillExists()

    def test_regular_user_is_forbidden_from_changing_data(self):
        self.client.force_login(self.regular)

        self.assertEqual(self.client.get(self.create_url).status_code, 403)
        self.assertEqual(self.client.get(self.edit_url).status_code, 403)
        response = self.client.post(self.delete_url, {"secret": self.SECRET})
        self.assertEqual(response.status_code, 403)
        self.assertExperienceStillExists()

    def test_editor_can_edit_experience(self):
        self.client.force_login(self.editor)

        self.assertEqual(self.client.get(self.edit_url).status_code, 200)
        response = self.client.post(
            self.edit_url,
            {
                "title": "Asisten Dosen PBP (diperbarui)",
                "description": self.experience.description,
                "category": "part-time",
                "secret": self.SECRET,
            },
        )
        self.assertRedirects(response, self.list_url)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Asisten Dosen PBP (diperbarui)")

    def test_editor_cannot_create_or_delete(self):
        self.client.force_login(self.editor)

        self.assertEqual(self.client.get(self.create_url).status_code, 403)
        response = self.client.post(self.delete_url, {"secret": self.SECRET})
        self.assertEqual(response.status_code, 403)
        self.assertExperienceStillExists()

    def test_owner_can_create_and_delete(self):
        self.client.force_login(self.owner)

        self.assertEqual(self.client.get(self.create_url).status_code, 200)
        response = self.client.post(self.delete_url, {"secret": self.SECRET})
        self.assertRedirects(response, self.list_url)
        self.assertFalse(Experience.objects.filter(pk=self.experience.pk).exists())

    def test_action_buttons_follow_user_role(self):
        edit_link = f'href="{self.edit_url}"'

        self.client.force_login(self.regular)
        response = self.client.get(self.list_url)
        self.assertNotContains(response, edit_link)
        self.assertNotContains(response, "Tambah Experience")
        self.assertNotContains(response, "Hapus Experience")

        self.client.force_login(self.editor)
        response = self.client.get(self.list_url)
        self.assertContains(response, edit_link)
        self.assertNotContains(response, "Tambah Experience")
        self.assertNotContains(response, "Hapus Experience")

        self.client.force_login(self.owner)
        response = self.client.get(self.list_url)
        self.assertContains(response, edit_link)
        self.assertContains(response, "Tambah Experience")
        self.assertContains(response, "Hapus Experience")


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
