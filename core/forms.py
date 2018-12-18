"""
    Formularios para la manipulación de los modelos de la
    app.

    Autores:
        - Emilio Sánchez Catalán <esc00019@gmail.com>.

    Version: 1.0.
"""

from django import forms
from django.contrib.admin.widgets import AdminFileWidget

from core.models import Tutor2

class CreateTutor2Form(forms.ModelForm):

    """
        Formulario para crear un tutor secundario o editarlo.
    """

    class Meta:
        model = Tutor2
        fields = [
            'name',
            'departament',
            'area',
            'curriculum_vitae'
        ]
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'departament': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'area': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'curriculum_vitae': AdminFileWidget(
                attrs={'class': 'form-control-file'}
            )
        }

    def __init__(self, *args, **kwargs):
        super(CreateTutor2Form, self).__init__(*args, **kwargs)
        self.fields['curriculum_vitae'].required = False
        self.__custom_departament()
        self.__custom_area()

    def __custom_departament(self):
        self.fields['departament'].empty_label = "Selecciona el departamento"

    def __custom_area(self):
        self.fields['area'].empty_label = "Selecciona el area"
