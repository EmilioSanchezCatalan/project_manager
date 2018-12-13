from django import forms
from .models import AnnouncementsTfg

class FilterAnnouncementsForm(forms.Form):
    name = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Título'}
    ))

class CreateAnnouncementsForm(forms.ModelForm):

    class Meta:
        model = AnnouncementsTfg
        fields = [
            'name'
        ]
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Nombre de la convocatoria'
                }
            )
        }