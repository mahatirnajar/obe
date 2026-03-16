from django import forms
from .models import Kontak


class KontakForm(forms.ModelForm):
    class Meta:
        model = Kontak
        fields = ['nama', 'email', 'subjek', 'pesan']
        widgets = {
            'nama': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nama lengkap Anda',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@example.com',
            }),
            'subjek': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Subjek pesan',
            }),
            'pesan': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Tuliskan pesan Anda di sini...',
                'rows': 5,
            }),
        }
        labels = {
            'nama': 'Nama',
            'email': 'Email',
            'subjek': 'Subjek',
            'pesan': 'Pesan',
        }
