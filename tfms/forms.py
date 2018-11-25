from django import forms
from django.contrib.auth.models import User
from core.models import Masters, Areas
from .models import Tfms

class FilterPublicTfmForm(forms.Form):
    name_project = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Título'}
    ))
    formation_project = forms.ModelChoiceField(
        queryset=Masters.objects.all(),
        empty_label="Master",
        required=False, 
        widget=forms.Select(
            attrs={'class': 'form-control'}
        )
    )

class FilterTeacherTfmForm(forms.Form):
    search_text = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Título'}
    ))
    formation_project = forms.ModelChoiceField(
        queryset=Masters.objects.all(),
        empty_label="Masters",
        required=False, 
        widget=forms.Select(
            attrs={'class': 'form-control'}
        )
    )
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(FilterTeacherTfmForm, self).__init__(*args, **kwargs)
        self.fields["formation_project"].queryset = self.user.userinfos.departaments.masters.all()

class FilterDepartamentTfmForm(forms.Form):
    search_text = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Título'}
    ))
    formation_project = forms.ModelChoiceField(
        queryset=Masters.objects.all(),
        empty_label="Masters",
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
        super(FilterDepartamentTfmForm, self).__init__(*args, **kwargs)
        self.fields["formation_project"].queryset = self.user.userinfos.departaments.master.all()
        self.fields["area"].queryset = self.user.userinfos.departaments.areas.all()
        self.fields["tutor"].queryset = User.objects.filter(userinfos__departaments = self.user.userinfos.departaments, groups__name="Teachers")


class CreateTfmForm(forms.ModelForm):

    class Meta:
        model = Tfms
        fields = [
            'title',
            'masters',
            'type',
            'mode',
            'objectives',
            'methodology',
            'language',
            'knowledge',
            'docs_and_forms',
            'tutor1'
        ]
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Nombre del proyecto',
                }
            ),
            'masters': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'type': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'mode': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'language': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Español, Ingles ...'
                }
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
            'knowledge': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 5
                }
            ),
            'tutor1': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        self.user = user
        super(CreateTfmForm, self).__init__(*args, **kwargs)
        self.fields['tutor1'].required = False
        self.__customMasters(user)
        self.__customType()
        self.__customMode()

    def __customMasters(self, user=None):
        self.fields['masters'].empty_label = "Selecciona la titulación"
        if user is not None:
            self.fields['masters'].queryset = user.userinfos.departaments.masters.all()

    def __customType(self):
        CHOICES = (
            ("", "Selecciona el tipo"),
            (Tfms.TYPE_BUSINESS, 'Empresa'),
            (Tfms.TYPE_UNI, 'Universidad'),
        )
        self.fields['type'] = forms.ChoiceField(
            widget=forms.Select(attrs={'class': 'form-control'}),
            choices=CHOICES
        )
    
    def __customMode(self):
        CHOICES = (
            ("", "Selecciona la modalidad"),
            (Tfms.MODE_INVESTIGATOR, 'Investigador'),
            (Tfms.MODE_PROFESSIONALIZING, 'Profesionalizante')
        )
        self.fields['mode'] = forms.ChoiceField(
            widget=forms.Select(attrs={'class': 'form-control'}),
            choices=CHOICES
        )