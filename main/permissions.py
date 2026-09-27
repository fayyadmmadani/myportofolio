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
