from django.db import models
from django.utils import timezone
import os

# Create your models here.
class Marca(models.Model):
    nombre = models.CharField(max_length=30, null=False, blank=False)

    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    nombre = models.CharField(max_length=30, null=False, blank=False)

    def __str__(self):
        return self.nombre

def producto_image_path(instance, filename):
    now = timezone.now()
    timestamp = now.strftime("%d/%m/%Y %H:%M:%S")
    extension = os.path.splitext(filename)[1]
    nombre_producto_slug = instance.nombre.replace(" ", "_").lower()
    new_filename = f"{nombre_producto_slug}_{timestamp}{extension}"

    return os.path.join('producto', new_filename)

class Producto(models.Model):
    nombre = models.CharField(max_length=15, null=False, blank=False)
    descripcion = models.TextField(null=False, blank=False)
    precio = models.DecimalField(max_digits=11, decimal_places=2, null=False, blank=False)
    cantidad = models.IntegerField(null=False, blank=False)
    marca = models.ForeignKey(Marca, null=True, on_delete=models.SET_NULL)
    categoria = models.ForeignKey(Categoria, null=True, on_delete=models.SET_NULL)
    imagen1 = models.ImageField(upload_to=producto_image_path, null=False, blank=False)
    imagen2 = models.ImageField(upload_to=producto_image_path, null=True, blank=True)
    imagen3 = models.ImageField(upload_to=producto_image_path, null=True, blank=True)
