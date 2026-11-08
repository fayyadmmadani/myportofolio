"""Utilitas otorisasi untuk membedakan hak akses tiap peran pengguna.

Peran yang dikenali aplikasi ini:

- Pengunjung (anonim) : hanya dapat membaca data.
- Pengguna biasa      : membaca data serta memberi/membatalkan star.
- Editor              : hak pengguna biasa + mengubah data portofolio.
- Pemilik (superuser) : seluruh hak, termasuk membuat dan menghapus data.

Peran Editor ditentukan lewat keanggotaan Django Group bernama ``Editor``.
Grup tersebut dibuat otomatis oleh migrasi ``0005_create_editor_group``,
sedangkan penetapan anggotanya dilakukan lewat Django Admin (``/admin``).
"""

from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    message = "Only the portfolio owner can change projects."

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_superuser
        )


class IsOwnerOrEditorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        return (
            request.method in ("PUT", "PATCH")
            and request.user.groups.filter(name="Editor").exists()
        )


EDITOR_GROUP_NAME = "Editor"


def is_editor(user):
    """Mengembalikan True jika ``user`` tergabung dalam grup Editor."""
    return (
        user.is_authenticated
        and user.groups.filter(name=EDITOR_GROUP_NAME).exists()
    )


def can_edit(user):
    """Mengembalikan True jika ``user`` berhak mengubah data portofolio.

    Berlaku untuk pemilik portofolio (superuser) maupun Editor.
    """
    return user.is_authenticated and (user.is_superuser or is_editor(user))


def can_create_or_delete(user):
    """Mengembalikan True jika ``user`` berhak membuat atau menghapus data.

    Hanya pemilik portofolio (superuser) yang diizinkan.
    """
    return user.is_authenticated and user.is_superuser
