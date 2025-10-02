from django import forms
from .models import *

class DomicilioForm(forms.ModelForm):
    class Meta:
        model = Domicilio
        fields= ['estado',
                   'municipio',
                   'colonia',
                   'cp',
                   'calle',
                   'ne',
                   'ni',
                   'referencia']
        widgets= {'cp': forms.NumberInput(),
                  'ne': forms.NumberInput(),
                  'referencia': forms.Textarea()}

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['first_name',
                   'last_name',
                   'username',
                   'email',
                   'celular',
                   'password',
                  'rol']
        widgets = {'email': forms.EmailInput(),
                   'password': forms.PasswordInput()}

class RegistroForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['username',
                  'email',
                  'password']
        widgets = {'email': forms.EmailInput(),
                   'password': forms.PasswordInput()}


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['first_name',
                   'last_name',
                   'username',
                   'email',
                   'celular']
        widgets = {'email': forms.EmailInput()}
