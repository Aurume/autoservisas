from .models import UzsakymoApzvalga
from django import forms

class UzsakymoApzvalgaForm(forms.ModelForm):
    class Meta:
        model = UzsakymoApzvalga
        fields = ('uzsakymas', 'vartotojas', 'atsiliepimas')
        widgets = {'uzsakymas': forms.HiddenInput(), 'vartotojas': forms.HiddenInput()}