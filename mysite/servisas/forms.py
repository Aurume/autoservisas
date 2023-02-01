from django.forms import DateInput

from .models import UzsakymoApzvalga, Profilis, Uzsakymas
from django import forms
from django.contrib.auth.models import User

class UzsakymoApzvalgaForm(forms.ModelForm):
    class Meta:
        model = UzsakymoApzvalga
        fields = ('uzsakymas', 'vartotojas', 'atsiliepimas')
        widgets = {'uzsakymas': forms.HiddenInput(), 'vartotojas': forms.HiddenInput()}

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfilisUpdateForm(forms.ModelForm):
    class Meta:
        model = Profilis
        fields = ['foto']


class ManoDateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'

class UzsakymaiVartotojoCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Uzsakymas
        fields = ['automobilis', 'terminas', 'status']
        widgets = {'terminas': ManoDateTimeInput()}