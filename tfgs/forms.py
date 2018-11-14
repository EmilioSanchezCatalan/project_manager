from django import forms
from core.models import Carrers, Departaments, Skills
from .models import Tfgs
from login.models import Userinfos

class FilterPublicTfgForm(forms.Form):
    name_project = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Título'}
    ))
    formation_project = forms.ModelChoiceField(
        queryset=Carrers.objects.all(),
        empty_label="Título",
        required=False, 
        widget=forms.Select(
            attrs={'class': 'form-control'}
        )
    )

class FilterTeacherTfgForm(forms.Form):
    search_text = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Título'}
    ))

class CreateTfgForm(forms.ModelForm):

    class Meta:
        model = Tfgs
        fields = [
            'title',
            'carrers',
            'itineraries',
            'mentions',
            'type',
            'mode',
            'is_team',
            'objectives',
            'methodology',
            'docs_and_forms',
            'skills'
        ]
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'inputTitle',
                    'placeholder': 'Nombre del proyecto'
                }
            ),
            'carrers': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'itineraries': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'mentions': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'mode': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'is_team': forms.CheckboxInput(
                attrs={'class': 'switch'}
            ),
            'objectives': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 5
                }
            ),
            'methodology': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 5
                }
            ),
            'docs_and_forms': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 5
                }
            ),
            'skills': forms.CheckboxSelectMultiple(
                attrs={'class': 'form-check-input'}
            )

        }

    def __init__(self, *args, **kwargs):
        super(CreateTfgForm, self).__init__(*args, **kwargs)
        user = kwargs['instance']
        self.__customCarrer(user)
        self.__customItinerarie()
        self.__customMention()
        self.__customType()
        self.__customMode()

    def __customCarrer(self, user):
        self.fields['carrers'].empty_label = "Selecciona la titulación"
        self.fields['carrers'].queryset = user.userinfos.departaments.carrers.all()

    def __customItinerarie(self):
        self.fields['itineraries'].empty_label = "Selecciona el itinerario"
        self.fields['itineraries'].required = False

    def __customMention(self):
        self.fields['mentions'].empty_label = "Selecciona la mención"
        self.fields['mentions'].required = False

    def __customType(self):
        CHOICES = (
            ("", "Selecciona el tipo"),
            (Tfgs.TYPE_GENERAL, 'General'),
            (Tfgs.TYPE_ESPECIFIC, 'Específico'),
        )
        self.fields['type'] = forms.ChoiceField(
            widget=forms.Select(attrs={'class': 'form-control'}),
            choices=CHOICES
        )
    
    def __customMode(self):
        CHOICES = (
            ("", "Selecciona la modalidad"),
            (Tfgs.MODE_EXP_THEORETICAL, 'Trabajo teórico/experimental'),
            (Tfgs.MODE_ING_PROYECT, 'Proyecto de Ingeniería'),
            (Tfgs.MODE_TECHNICAL_STUDY, 'Estudio técnico')
        )
        self.fields['mode'] = forms.ChoiceField(
            widget=forms.Select(attrs={'class': 'form-control'}),
            choices=CHOICES
        )