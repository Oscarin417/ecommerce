from django.db import models
from producto.models import Producto
from usuario.models import Usuario

# Create your models here.
class Pasarela(models.Model):
    nombre = models.CharField(max_length=50, null=False, blank=False)
    contexto = models.TextField(null=True, blank=True, default={})

class Venta(models.Model):
    usuario = models.ForeignKey(Usuario, null=True, on_delete=models.SET_NULL)
    producto = models.ForeignKey(Producto, null=True, on_delete=models.SET_NULL)
    cantidad = models.IntegerField(null=False, blank=False)
    fecha_creacion = models.DateTimeField(null=False, blank=False)
    total = models.DecimalField(max_digits=11, decimal_places=2, null=False, blank=False)
    estatus = models.CharField(max_length=1, null=False, blank=False, default='P') #C cancelado, P en proceso, S completado
    pasarela = models.ForeignKey(Pasarela, null=True, on_delete=models.SET_NULL)
    atributos = models.TextField(default={})

    def estatus_completo(self):
        texto = ''
        if self.estatus == 'P':
            texto='En proceso'
        elif self.estatus == 'C':
            texto='Cancelado'
        else:
            texto='Completado'

        return texto
