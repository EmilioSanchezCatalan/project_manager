"""
    Formularios para la manipulación de los modelos de la
    app.

    Autores:
        - Emilio Sánchez Catalán <esc00019@gmail.com>.

    Version: 1.0.
"""

from django import forms
from login.models import Students

class CreateStudentForm(forms.ModelForm):

    """
        Formulario de creación de estudiantes
    """
    class Meta:
        model = Students
        fields = [
            'name',
            'dni',
            'phone',
            'email'
        ]
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'email': forms.EmailInput(
                attrs={'class': 'form-control'}
            ),
            'dni': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'phone': forms.TextInput(
                attrs={'class': 'form-control'}
            )
        }
