from django.forms import ModelForm, TextInput, Textarea, URLInput, NumberInput, DateTimeInput

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