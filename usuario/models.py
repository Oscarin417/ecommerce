from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Domicilio(models.Model):
    estado = models.CharField(max_length=50, null=True, blank=True)
    municipio = models.CharField(max_length=50, null=True, blank=True)
    colonia = models.CharField(max_length=50, null=True, blank=True)
    cp = models.CharField(max_length=5, null=True, blank=True, verbose_name="Codigo postal")
    calle = models.CharField(max_length=50, null=True, blank=True)
    ne = models.IntegerField(null=True, blank=True, verbose_name="Numero exterior")
    ni = models.CharField(max_length=5, null=True, blank=True, verbose_name="Numero interior")
    referencia = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.calle} #{self.ne}, {self.colonia}, {self.municipio}"

    def numero_interior(self):
        numero = ''
        if self.ni == None:
            numero = 'N/A'
        else:
            numero = self.ni
        return numero

class Usuario(AbstractUser):
    ROLES = [
        ('', 'Seleccione un rol'),
        (1, 'Administrador'),
        (2, 'Empleado'),
        (3, 'Cliente')
    ]
    rol = models.IntegerField(choices=ROLES, null=True, blank=True)
    celular = models.CharField(max_length=13, null=True, blank=True)
    domicilio = models.ForeignKey(Domicilio, null=True, on_delete=models.SET_NULL)
    atributos = models.TextField(default={})

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="usuario_set",  # <--- CAMBIO AQUÍ
        related_query_name="usuario",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="usuario_set",  # <--- CAMBIO AQUÍ
        related_query_name="usuario",
    )

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def roles(self):
        rol_completo = ''
        if self.rol == 1:
            rol_completo = 'Administrador'
        elif self.rol == 2:
            rol_completo = 'Empleado'
        else:
            rol_completo = 'Cliente'

        return rol_completo
