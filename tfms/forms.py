"""
    Formularios para la manipulación de TFMs.

    Autores:
        - Emilio Sánchez Catalán <esc00019@gmail.com>.

    Version: 1.0.
"""

import datetime
from django import forms
from django.contrib.auth.models import User
from ckeditor.widgets import CKEditorWidget
from core.models import Masters, Areas, Departaments
from announcements.models import AnnouncementsTfm
from tfms.models import Tfms

class FilterPublicCenterForm(forms.Form):

    """
        Filtros para el listado de Centros

        Atributos:
            center_name(forms.CharField): Input tipo Text para el nombre del Centro.

    """
    center_name = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Título'}
    ))

class FilterPublicTfmForm(forms.Form):

    """
        Filtros para el listado de TFMs público.

        Atributos:
            name_proyect(forms.CharField): Input tipo Text para el titulo dle TFM.
            formation_project(forms.ModelChoiceField): Selector para la elección de la titulación.

    """

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

    def __init__(self, *args, **kwargs):
        self.center = kwargs.pop("center")
        super(FilterPublicTfmForm, self).__init__(*args, **kwargs)
        self.fields["formation_project"].queryset = self.center.masters.all()

class FilterPublicHistoryTfmForm(forms.Form):

    """
        Filtros para el historico de TFMs.

        Atributos:
            name_proyect(forms.CharField): Input tipo Text para el titulo dle TFM.
            formation_project(forms.ModelChoiceField): Selector para la elección de la titulación.

    """
    name_project = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Título'}
    ))
    formation_project = forms.ModelChoiceField(
        queryset=Masters.objects.all(),
        empty_label="Titulación",
        required=False,
        widget=forms.Select(
            attrs={'class': 'form-control'}
        )
    )

    announcements = forms.ModelChoiceField(
        queryset=AnnouncementsTfm.objects.all(),
        empty_label="Convocatorias",
        required=False,
        widget=forms.Select(
            attrs={'class': 'form-control'}
        )
    )

    def __init__(self, *args, **kwargs):
        self.center = kwargs.pop("center")
        super(FilterPublicHistoryTfmForm, self).__init__(*args, **kwargs)
        self.fields["formation_project"].queryset = self.center.masters.all()
        now = datetime.datetime.now()
        earlier = now - datetime.timedelta(days=730)
        self.fields["announcements"].queryset = AnnouncementsTfm.objects.filter(
            updatedAt__range=(earlier, now),
            centers_id=self.center.id
        )

class FilterTeacherTfmForm(forms.Form):

    """
        Filtros para el listado de TFMs para profesores.

        Atributos:
            search_text(forms.CharField): Input tipo Text para el titulo dle TFM.
            formation_project(forms.ModelChoiceField): Selector para la elección de la titulación.
            validation_state(forms.ChoiceField): Selector para elección del estado de la validación.

    """

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
    validation_state = forms.ChoiceField(
        choices=(
            ("", "Selecciona el estado de la validación"),
            (Tfms.NOT_VALIDATED, "❔ Aún no validado"),
            (Tfms.DEPARTAMENT_VALIDATION, "✔️ Validado por departamento"),
            (Tfms.CENTER_VALIDATION, "✔️✔️ Validado por el centro"),
            (Tfms.FAIL_VALIDATION, "❌ Projecto no aceptado")
        ),
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

    """
        Filtros para el listado de TFMs para departamentos.

        Atributos:
            search_text(forms.CharField): Input tipo Text para el titulo dle TFM.
            formation_project(forms.ModelChoiceField): Selector para la elección de la titulación.
            area(forms.ModelChoiceField): Selector para elección del area del tutor que
                                          ha creado el TFM.
            tutor(forms.ModelChoiceField): Selector para la elección dle tutor que ha creado el TFM.

    """

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

    status = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': 'form-control'}
        ),
        required=False,
        choices=(
            ("", "Selecciona el estado de la validación"),
            (Tfms.NOT_VALIDATED, "❔ No validado"),
            (Tfms.DEPARTAMENT_VALIDATION, "✔️ Validado"),
            (Tfms.FAIL_VALIDATION, "❌ Rechazado")
        )
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(FilterDepartamentTfmForm, self).__init__(*args, **kwargs)
        self.fields["formation_project"].queryset = Masters.objects.filter(
            tfms__tutor1__userinfos__departaments=self.user.userinfos.departaments
        ).distinct()
        self.fields["area"].queryset = self.user.userinfos.departaments.areas.all()
        self.fields["tutor"].queryset = User.objects.filter(
            userinfos__departaments=self.user.userinfos.departaments,
            groups__name="Teachers"
        )

class FilterCenterTfmForm(forms.Form):

    """
        Filtros para el listado de TFMs para centros.

        Atributos:
            search_text(forms.CharField): Input tipo Text para el titulo dle TFM.
            formation_project(forms.ModelChoiceField): Selector para la elección de la titulación.
            departament(forms.ModelChoiceField): Selector para elección del departamento del tutor
                                                 que ha creado el TFM.
            tutor(forms.ModelChoiceField): Selector para la elección dle tutor que ha creado el TFM.

    """

    search_text = forms.CharField(required=False, widget=forms.TextInput(
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

    status = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': 'form-control'}
        ),
        required=False,
        choices=(
            ("", "Selecciona el estado de la validación"),
            (Tfms.NOT_VALIDATED, "❔ No validado"),
            (Tfms.DEPARTAMENT_VALIDATION, "✔️ Validado"),
            (Tfms.FAIL_VALIDATION, "❌ Rechazado")
        )
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(FilterCenterTfmForm, self).__init__(*args, **kwargs)
        self.fields["departament"].queryset = Departaments.objects.filter(
            masters__in=self.user.userinfos.centers.masters.all()
        ).distinct()
        self.fields["formation_project"].queryset = self.user.userinfos.centers.masters.all()
        self.fields["tutor"].queryset = User.objects.filter(
            groups__name="Teachers",
            tfms__masters__in=self.user.userinfos.centers.masters.all(),
            tfms__departament_validation=True,
        ).distinct()

class CreateTfmForm(forms.ModelForm):

    """
        Formulario para la creación y edición de los TFMs.
    """

    class Meta:
        model = Tfms
        fields = [
            'title',
            'masters',
            'type',
            'objectives',
            'methodology',
            'language',
            'knowledge',
            'docs_and_forms',
            'tutor1',
            'draft'
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
            'draft': forms.CheckboxInput(
                attrs={'class': 'switch'}
            ),
            'type': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'language': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Español, Ingles ...'
                }
            ),
            'objectives': CKEditorWidget(),
            'methodology': CKEditorWidget(),
            'docs_and_forms': CKEditorWidget(),
            'knowledge': CKEditorWidget(),
            'tutor1': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        self.user = user
        super(CreateTfmForm, self).__init__(*args, **kwargs)
        self.fields['tutor1'].required = False
        self.__custom_masters(user)
        self.__custom_type()

    def __custom_masters(self, user=None):
        self.fields['masters'].empty_label = "Selecciona la titulación"
        if user is not None:
            self.fields['masters'].queryset = user.userinfos.departaments.masters.all()

    def __custom_type(self):
        choices = (
            ("", "Selecciona el tipo"),
            (Tfms.TYPE_BUSINESS, Tfms.TYPE_TEXT_BUSINESS),
            (Tfms.TYPE_UNI, Tfms.TYPE_TEXT_UNI),
        )
        self.fields['type'] = forms.ChoiceField(
            widget=forms.Select(attrs={'class': 'form-control'}),
            choices=choices
        )
