"""
    Formularios para la manipulación de las convocatorias.

    Autores:
        - Emilio Sánchez Catalán <esc00019@gmail.com>.

      Version: 1.0.
"""
from django import forms
from .models import AnnouncementsTfg

class FilterAnnouncementsForm(forms.Form):

    """
        Formulario del listado de convocatorias.
        name(forms.CharField): nombre de la convocatoria.
    """

    name = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Título'}
    ))

class CreateAnnouncementsForm(forms.ModelForm):

    """
        Formulario para la creación de convocatorias.
    """

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