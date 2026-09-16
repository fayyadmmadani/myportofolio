from django.forms import ModelForm, TextInput, Textarea, URLInput, NumberInput

from main.models import Project

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ["title", "description", "thumbnail", "order"]

        labels = {
            "title": "Nama Proyek",
            "description": "Deskripsi Proyek",
            "thumbnail": "URL Thumbnail Proyek",
            "order": "Urutan Tampil",
        }

        widgets = {
            "title": TextInput(attrs={"placeholder": "Portfolio Website", "maxlength": 255}),
            "description": Textarea(attrs={"placeholder": "Ceritakan Proyekmu", "rows": 3}),
            "thumbnail": URLInput(attrs={"placeholder": "https://.../thumbnail.png"}),
            "order": NumberInput(attrs={"placeholder": "0"}),
        }