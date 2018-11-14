from django import forms
from .models import Students

class CreateStudentForm(forms.ModelForm):
    
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

    def __init__(self, *args, **kwargs):
        super(CreateStudentForm, self).__init__(*args, **kwargs)
        self.fields['name'].id = 'id_student_name'