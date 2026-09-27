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


@override_settings(EDIT_SECRET="rahasia-uji")
class ProjectAccessTest(TestCase):
    """Menguji hak akses keempat peran, fitur star, dan API pada Projects."""

    SECRET = "rahasia-uji"

    def setUp(self):
        self.project = Project.objects.create(
            title="Portfolio Website",
            description="Situs portofolio pribadi dibangun dengan Django.",
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

        self.list_url = reverse("main:show_projects")
        self.api_url = reverse("main:get_projects_json")
        self.create_url = reverse("main:create_project")
        self.edit_url = reverse("main:edit_project", args=[self.project.id])
        self.delete_url = reverse("main:delete_project", args=[self.project.id])
        self.star_url = reverse("main:toggle_star", args=[self.project.id])

    def assertProjectStillExists(self):
        self.assertTrue(Project.objects.filter(pk=self.project.pk).exists())

    # ---------- hak akses CRUD ----------

    def test_anonymous_can_read_but_must_login_to_act(self):
        self.assertEqual(self.client.get(self.list_url).status_code, 200)

        for url in (self.create_url, self.edit_url):
            response = self.client.get(url)
            self.assertRedirects(
                response, f"/login/?next={url}", fetch_redirect_response=False
            )

        for url in (self.delete_url, self.star_url):
            response = self.client.post(url, {"secret": self.SECRET})
            self.assertRedirects(
                response, f"/login/?next={url}", fetch_redirect_response=False
            )

        self.assertProjectStillExists()
        self.assertEqual(self.project.starred_by.count(), 0)

    def test_regular_user_is_forbidden_from_changing_data(self):
        self.client.force_login(self.regular)

        self.assertEqual(self.client.get(self.create_url).status_code, 403)
        self.assertEqual(self.client.get(self.edit_url).status_code, 403)
        response = self.client.post(self.delete_url, {"secret": self.SECRET})
        self.assertEqual(response.status_code, 403)
        self.assertProjectStillExists()

    def test_editor_can_edit_project(self):
        self.client.force_login(self.editor)

        self.assertEqual(self.client.get(self.edit_url).status_code, 200)
        response = self.client.post(
            self.edit_url,
            {
                "title": "Portfolio Website v2",
                "description": self.project.description,
                "thumbnail": "",
                "order": 0,
                "secret": self.SECRET,
            },
        )
        self.assertRedirects(response, self.list_url)
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "Portfolio Website v2")

    def test_editor_cannot_create_or_delete(self):
        self.client.force_login(self.editor)

        self.assertEqual(self.client.get(self.create_url).status_code, 403)
        response = self.client.post(self.delete_url, {"secret": self.SECRET})
        self.assertEqual(response.status_code, 403)
        self.assertProjectStillExists()

    def test_owner_can_create_and_delete(self):
        self.client.force_login(self.owner)

        self.assertEqual(self.client.get(self.create_url).status_code, 200)
        response = self.client.post(self.delete_url, {"secret": self.SECRET})
        self.assertRedirects(response, self.list_url)
        self.assertFalse(Project.objects.filter(pk=self.project.pk).exists())

    def test_action_buttons_follow_user_role(self):
        edit_link = f'href="{self.edit_url}"'

        self.client.force_login(self.regular)
        response = self.client.get(self.list_url)
        self.assertContains(response, f'action="{self.star_url}"')
        self.assertNotContains(response, edit_link)
        self.assertNotContains(response, "Tambah Proyek")
        self.assertNotContains(response, "Hapus Proyek")

        self.client.force_login(self.editor)
        response = self.client.get(self.list_url)
        self.assertContains(response, edit_link)
        self.assertNotContains(response, "Tambah Proyek")
        self.assertNotContains(response, "Hapus Proyek")

        self.client.force_login(self.owner)
        response = self.client.get(self.list_url)
        self.assertContains(response, edit_link)
        self.assertContains(response, "Tambah Proyek")
        self.assertContains(response, "Hapus Proyek")

    # ---------- fitur star ----------

    def test_star_toggles_and_is_limited_to_one_per_user(self):
        self.client.force_login(self.regular)

        self.client.post(self.star_url)
        self.assertTrue(self.project.starred_by.filter(pk=self.regular.pk).exists())
        self.assertEqual(self.project.starred_by.count(), 1)

        self.client.post(self.star_url)
        self.assertEqual(self.project.starred_by.count(), 0)

    def test_star_counts_each_user_separately(self):
        for user in (self.regular, self.editor, self.owner):
            self.client.force_login(user)
            self.client.post(self.star_url)

        self.assertEqual(self.project.starred_by.count(), 3)

    def test_star_requires_post(self):
        self.client.force_login(self.regular)

        response = self.client.get(self.star_url)
        self.assertRedirects(response, self.list_url)
        self.assertEqual(self.project.starred_by.count(), 0)

    def test_star_status_and_count_are_displayed(self):
        self.client.force_login(self.regular)
        self.client.post(self.star_url)

        response = self.client.get(self.list_url)
        self.assertContains(response, "is-starred")
        self.assertContains(response, "Unstar")
        self.assertContains(response, '<span class="star-count">1</span>', html=True)

    # ---------- API ----------

    def test_projects_json_does_not_leak_sensitive_data(self):
        self.project.starred_by.add(self.regular)

        response = self.client.get(self.api_url)
        self.assertEqual(response.status_code, 200)

        fields = response.json()[0]["fields"]
        self.assertEqual(fields["title"], self.project.title)
        self.assertEqual(fields["starred_by"], [["pengguna"]])
        self.assertNotIn("password", response.content.decode())
        self.assertNotIn("pbkdf2", response.content.decode())


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
