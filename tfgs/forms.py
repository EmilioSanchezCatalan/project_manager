from django import forms
from django.contrib.auth.models import User
from core.models import Carrers, Departaments, Skills, Areas
from .models import Tfgs
from login.models import Userinfos

class FilterPublicTfgForm(forms.Form):
    name_project = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Título'}
    ))
    formation_project = forms.ModelChoiceField(
        queryset=Carrers.objects.all(),
        empty_label="Titulación",
        required=False, 
        widget=forms.Select(
            attrs={'class': 'form-control'}
        )
    )

class FilterTeacherTfgForm(forms.Form):
    search_text = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Título'}
    ))
    formation_project = forms.ModelChoiceField(
        queryset=Carrers.objects.all(),
        empty_label="Titulación",
        required=False, 
        widget=forms.Select(
            attrs={'class': 'form-control'}
        )
    )
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(FilterTeacherTfgForm, self).__init__(*args, **kwargs)
        self.fields["formation_project"].queryset = self.user.userinfos.departaments.carrers.all()

class FilterDepartamentTfgForm(forms.Form):
    search_text = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Título'}
    ))
    formation_project = forms.ModelChoiceField(
        queryset=Carrers.objects.all(),
        empty_label="Titulación",
        required=False, 
        widget=forms.Select(
            attrs={'class': 'form-control'}
        )
    )
    area = forms.ModelChoiceField(
        queryset=Areas.objects.all(),
        empty_label="Area de conocimiento",
        required=False,
        widget=forms.Select(
            attrs={'class': 'form-control'}
        )
    )
    tutor = forms.ModelChoiceField(
        queryset=User.objects.all(),
        empty_label="Tutor",
        required=False,
        widget=forms.Select(
            attrs={'class': 'form-control'}
        )
    )
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(FilterDepartamentTfgForm, self).__init__(*args, **kwargs)
        self.fields["formation_project"].queryset = self.user.userinfos.departaments.carrer.all()
        self.fields["area"].queryset = self.user.userinfos.departaments.areas.all()
        self.fields["tutor"].queryset = User.objects.filter(userinfos__departaments = self.user.userinfos.departaments, groups__name="Teachers")

class FilterCenterTfgForm(forms.Form):
    search_text = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Título'}
    ))
    formation_project = forms.ModelChoiceField(
        queryset=Carrers.objects.all(),
        empty_label="Titulación",
        required=False, 
        widget=forms.Select(
            attrs={'class': 'form-control'}
        )
    )
    departament = forms.ModelChoiceField(
        queryset=Departaments.objects.all(),
        empty_label="Departamento",
        required=False,
        widget=forms.Select(
            attrs={'class': 'form-control'}
        )
    )
    tutor = forms.ModelChoiceField(
        queryset=User.objects.all(),
        empty_label="Tutor",
        required=False,
        widget=forms.Select(
            attrs={'class': 'form-control'}
        )
    )
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(FilterCenterTfgForm, self).__init__(*args, **kwargs)
        self.fields["formation_project"].queryset = self.user.userinfos.centers.carrers.all()
        self.fields["tutor"].queryset = User.objects.filter(groups__name="Teachers")

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
            'skills',
            'tutor1'
        ]
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Nombre del proyecto',
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
            ),
            'tutor1': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        self.user = user
        super(CreateTfgForm, self).__init__(*args, **kwargs)
        self.fields["tutor1"].required = False
        self.__customCarrer(user)
        self.__customItinerarie()
        self.__customMention()
        self.__customType()
        self.__customMode()
        self.__customSkills()

    def __customCarrer(self, user=None):
        self.fields['carrers'].empty_label = "Selecciona la titulación"
        if user is not None:
            self.fields['carrers'].queryset = user.userinfos.departaments.carrers.all()

    def __customItinerarie(self):
        self.fields['itineraries'].empty_label = "Selecciona el itinerario"

    def __customMention(self):
        self.fields['mentions'].empty_label = "Selecciona la mención"

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
    def __customSkills(self):
        self.fields['skills'].required = False