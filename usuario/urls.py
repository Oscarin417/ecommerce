from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('', usuario, name='usuario'),
    path('domicilio/', domicilio, name='domicilio'),
    path('crear/', usuario_store, name='usuario_crear'),
    re_path(r'editar/(?P<pk>\d+)/$', usuario_update, name='usuario_editar'),
    re_path(r'eliminar/(?P<pk>\d+)/$', usuario_destroy, name='usuario_eliminar'),
    path('perfil/', perfil, name='perfil')
]
