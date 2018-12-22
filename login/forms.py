"""
    Formularios para la manipulación de los modelos de la
    app.

    Autores:
        - Emilio Sánchez Catalán <esc00019@gmail.com>.

    Version: 1.0.
"""

from django import forms
from login.models import Students
from core.models import Centers

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

class ResetEmailForm(forms.Form):

    """
        Formulario para resetear la contraseña a traves de un correo
        electrónico.

        Atributos:
            email(forms.EmailField): correo electronico donde enviar
                                     el correo de restauración
    """

    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            'class': 'form-control',
            'placeholder': "email@example.com"
        }
    ))

class ResetPasswordForm(forms.Form):

    """
        Formulario para establecer la nueva contraseña.
    """

    new_password1 = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Nueva Contraseña'
        }
    ))

    new_password2 = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Repite Contraseña'
        }
    ))

class CenterLogoForm(forms.ModelForm):

    """
        Formulario para establecer una imagen de logo a un centro
    """

    class Meta():
        model = Centers
        fields = ['logo']
