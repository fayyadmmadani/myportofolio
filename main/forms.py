from django.core.exceptions import ValidationError
from django.forms import ModelForm, TextInput, Textarea, URLInput, NumberInput, DateTimeInput
from django.utils.html import strip_tags

from main.models import Project, Experience

class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = ["title", "description", "category", "thumbnail", "ended_at"]
        
        labels = {
            "title": "Nama Experience",
            "description": "Deskripsi Experience",
            "category": "Kategori Experience",
            "thumbnail": "URL Thumbnail Experience",
            "ended_at": "Tanggal Selesai (kosongkan jika masih berlangsung)"
        }
        
        widgets = {
            "title": TextInput(attrs={"placeholder": "Portfolio Website", "maxlength": 255}),
            "description": Textarea(attrs={"placeholder": "Ceritakan Proyekmu", "rows": 3}),
            "thumbnail": URLInput(attrs={"placeholder": "https://.../thumbnail.png"}),
            "ended_at": DateTimeInput(attrs={"type" : "datetime-local"})
        }

    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()
        if not title:
            raise ValidationError("Nama experience tidak boleh hanya berisi tag HTML.")
        return title

    def clean_description(self):
        description = strip_tags(self.cleaned_data["description"]).strip()
        if not description:
            raise ValidationError("Deskripsi experience tidak boleh hanya berisi tag HTML.")
        return description

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

    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()
        if not title:
            raise ValidationError("Nama proyek tidak boleh hanya berisi tag HTML.")
        return title

    def clean_description(self):
        return strip_tags(self.cleaned_data["description"]).strip()
