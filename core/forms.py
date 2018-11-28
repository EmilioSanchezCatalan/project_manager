from django import forms
from django.contrib.admin.widgets import AdminFileWidget

from .models import Tutor2

class CreateTutor2Form(forms.ModelForm):

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
        self.__customDepartament()
        self.__customArea()

    def __customDepartament(self):
        self.fields['departament'].empty_label = "Selecciona el departamento"

    def __customArea(self):
        self.fields['area'].empty_label = "Selecciona el area"
