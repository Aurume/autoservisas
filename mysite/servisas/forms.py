from .models import UzsakymoApzvalga
from django import forms

class UzsakymoApzvalgaForm(forms.ModelForm):
    class Meta:
        model = UzsakymoApzvalga
        fields = ('atsiliepimas', 'uzsakymas_id', 'klientas_id',)
        widgets = {'uzsakymas_id': forms.HiddenInput(), 'klientas_id': forms.HiddenInput()}