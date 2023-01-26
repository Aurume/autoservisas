from .models import UzsakymoApzvalga
from django import forms

class UzsakymoApzvalgaForm(forms.ModelForm):
    class Meta:
        model = UzsakymoApzvalga
        fields = ('apzvalga', 'automobilis', 'vartotojas',)
        widgets = {'automobilis': forms.HiddenInput(), 'vartotojas': forms.HiddenInput()}