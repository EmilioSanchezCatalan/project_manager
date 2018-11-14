from django import forms
from .models import Tutor2

class CreateTutor2Form(forms.ModelForm):

    class Meta:
        model = Tutor2
        fields = [
            'name',
            'departament',
            'area'
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
            )
        }
    
    def __init__(self, *args, **kwargs):
        super(CreateTutor2Form, self).__init__(*args, **kwargs)
        self.__customDepartament()
        self.__customArea()

    def __customDepartament(self):
        print('Entra')
        self.fields['departament'].empty_label = "Selecciona el departamento"
        self.fields['departament'].required = False

    def __customArea(self):
        self.fields['area'].empty_label = "Selecciona el area"
        self.fields['area'].required = False