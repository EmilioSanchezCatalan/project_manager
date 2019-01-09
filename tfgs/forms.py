"""
    Formularios para la manipulación de TFGs.

    Autores:
        - Emilio Sánchez Catalán <esc00019@gmail.com>.

    Version: 1.0.
"""
import datetime
from django import forms
from django.contrib.auth.models import User
from django.contrib.admin.widgets import AdminFileWidget
from ckeditor.widgets import CKEditorWidget
from core.models import Carrers, Departaments, Areas
from announcements.models import AnnouncementsTfg
from tfgs.models import Tfgs

class FilterPublicCenterForm(forms.Form):

    """
        Filtros para el listado de Centros

        Atributos:
            center_name(forms.CharField): Input tipo Text para el nombre del Centro.

    """
    center_name = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Título'}
    ))


class FilterPublicTfgForm(forms.Form):

    """
        Filtros para el listado de TFGs público.

        Atributos:
            name_proyect(forms.CharField): Input tipo Text para el titulo dle TFG.
            formation_project(forms.ModelChoiceField): Selector para la elección de la titulación.

    """
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

    def __init__(self, *args, **kwargs):
        self.center = kwargs.pop("center")
        super(FilterPublicTfgForm, self).__init__(*args, **kwargs)
        self.fields["formation_project"].queryset = self.center.carrers.all()

class FilterPublicHistoryTfgForm(forms.Form):

    """
        Filtros para el histórico de TFGs.

        Atributos:
            name_proyect(forms.CharField): Input tipo Text para el titulo dle TFG.
            formation_project(forms.ModelChoiceField): Selector para la elección de la titulación.

    """
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

    announcements = forms.ModelChoiceField(
        queryset=AnnouncementsTfg.objects.all(),
        empty_label="Convocatorias",
        required=False,
        widget=forms.Select(
            attrs={'class': 'form-control'}
        )
    )

    def __init__(self, *args, **kwargs):
        self.center = kwargs.pop("center")
        super(FilterPublicHistoryTfgForm, self).__init__(*args, **kwargs)
        self.fields["formation_project"].queryset = self.center.carrers.all()
        now = datetime.datetime.now()
        earlier = now - datetime.timedelta(days=730)
        self.fields["announcements"].queryset = AnnouncementsTfg.objects.filter(
            updatedAt__range=(earlier, now),
            centers_id=self.center.id
        )

class FilterTeacherTfgForm(forms.Form):

    """
        Filtros para el listado de TFGs para profesores.

        Atributos:
            search_text(forms.CharField): Input tipo Text para el titulo dle TFG.
            formation_project(forms.ModelChoiceField): Selector para la elección de la titulación.
            validation_state(forms.ChoiceField): Selector para elección del estado de la validación.

    """

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
    validation_state = forms.ChoiceField(
        choices=(
            ("", "Selecciona el estado de la validación"),
            (Tfgs.NOT_VALIDATED, "❔ Aún no validado"),
            (Tfgs.DEPARTAMENT_VALIDATION, "✔️ Validado por departamento"),
            (Tfgs.CENTER_VALIDATION, "✔️✔️ Validado por el centro"),
            (Tfgs.FAIL_VALIDATION, "❌ Projecto no aceptado")
        ),
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

    """
        Filtros para el listado de TFGs para departamentos.

        Atributos:
            search_text(forms.CharField): Input tipo Text para el titulo dle TFG.
            formation_project(forms.ModelChoiceField): Selector para la elección de la titulación.
            area(forms.ModelChoiceField): Selector para elección del area del tutor que
                                          ha creado el TFG.
            tutor(forms.ModelChoiceField): Selector para la elección dle tutor que ha creado el TFG.

    """

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
        self.fields["formation_project"].queryset = Carrers.objects.filter(
            tfgs__tutor1__userinfos__departaments=self.user.userinfos.departaments
        ).distinct()
        self.fields["area"].queryset = self.user.userinfos.departaments.areas.all()
        self.fields["tutor"].queryset = User.objects.filter(
            userinfos__departaments=self.user.userinfos.departaments,
            groups__name="Teachers"
        )

class FilterCenterTfgForm(forms.Form):

    """
        Filtros para el listado de TFGs para centros.

        Atributos:
            search_text(forms.CharField): Input tipo Text para el titulo dle TFG.
            formation_project(forms.ModelChoiceField): Selector para la elección de la titulación.
            departament(forms.ModelChoiceField): Selector para elección del departamento del tutor
                                                 que ha creado el TFG.
            tutor(forms.ModelChoiceField): Selector para la elección dle tutor que ha creado el TFG.

    """

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

    """
        Formulario para la creación y edición de los TFGs.
    """

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
            'tutor1',
            'team_memory',
            'draft'
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
            'draft': forms.CheckboxInput(
                attrs={'class': 'switch'}
            ),
            'team_memory': AdminFileWidget(
                attrs={'class': 'form-control-file'}
            ),
            'objectives': CKEditorWidget(),
            'methodology': CKEditorWidget(),
            'docs_and_forms': CKEditorWidget(),
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
        self.__custom_carrer(user)
        self.__custom_itinerarie()
        self.__custom_mention()
        self.__custom_type()
        self.__custom_mode()
        self.__custom_skills()

    def __custom_carrer(self, user=None):
        self.fields['carrers'].empty_label = "Selecciona la titulación"
        if user is not None:
            self.fields['carrers'].queryset = user.userinfos.departaments.carrers.all()

    def __custom_itinerarie(self):
        self.fields['itineraries'].empty_label = "Selecciona el itinerario"

    def __custom_mention(self):
        self.fields['mentions'].empty_label = "Selecciona la mención"

    def __custom_type(self):
        choices = (
            ("", "Selecciona el tipo"),
            (Tfgs.TYPE_GENERAL, Tfgs.TYPE_TEXT_GENERAL),
            (Tfgs.TYPE_ESPECIFIC, Tfgs.TYPE_TEXT_ESPECIFIC),
        )
        self.fields['type'] = forms.ChoiceField(
            widget=forms.Select(attrs={'class': 'form-control'}),
            choices=choices
        )

    def __custom_mode(self):
        choices = (
            ("", "Selecciona la modalidad"),
            (Tfgs.MODE_EXP_THEORETICAL, Tfgs.MODE_TEXT_EXP_THEORETICAL),
            (Tfgs.MODE_ING_PROYECT, Tfgs.MODE_TEXT_ING_PROYECT),
            (Tfgs.MODE_TECHNICAL_STUDY, Tfgs.MODE_TEXT_TECHNICAL_STUDY)
        )
        self.fields['mode'] = forms.ChoiceField(
            widget=forms.Select(attrs={'class': 'form-control'}),
            choices=choices
        )
    def __custom_skills(self):
        self.fields['skills'].required = False
