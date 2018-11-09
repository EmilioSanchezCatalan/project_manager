from django import forms
from core.models import Carrers

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
    