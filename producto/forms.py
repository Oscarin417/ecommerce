from django import forms
from .models import *

class MarcaForm(forms.ModelForm):
    class Meta:
        model = Marca
        fields = ['nombre']
        widgets = {'__all__'}

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']
        widgets = {'__all__'}

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre',
                  'descripcion',
                  'precio',
                  'cantidad',
                  'imagen1',
                  'imagen2',
                  'imagen3',
                  'categoria',
                  'marca']
        widgets = {'descripcion': forms.Textarea(),
                   'precio': forms.NumberInput(),
                   'cantidad': forms.NumberInput(),
                   'categoria': forms.Select(),
                   'marca': forms.Select()}
