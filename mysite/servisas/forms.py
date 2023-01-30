from .models import UzsakymoApzvalga, Profilis
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