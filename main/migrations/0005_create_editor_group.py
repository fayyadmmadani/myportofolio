"""Membuat Django Group ``Editor`` sebagai peran bawaan aplikasi.

Grup dibuat lewat migrasi (bukan hanya manual lewat Django Admin) supaya peran
ini selalu tersedia di setiap environment segera setelah ``manage.py migrate``
dijalankan. Penetapan anggota grup tetap dilakukan lewat Django Admin.
"""

from django.db import migrations

EDITOR_GROUP_NAME = "Editor"


def create_editor_group(apps, schema_editor):
    """Membuat grup Editor bila belum ada."""
    Group = apps.get_model("auth", "Group")
    Group.objects.get_or_create(name=EDITOR_GROUP_NAME)


def delete_editor_group(apps, schema_editor):
    """Menghapus grup Editor saat migrasi di-rollback."""
    Group = apps.get_model("auth", "Group")
    Group.objects.filter(name=EDITOR_GROUP_NAME).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0004_project_starred_by"),
        ("auth", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_editor_group, delete_editor_group),
    ]
