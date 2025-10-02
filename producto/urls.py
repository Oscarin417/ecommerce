from django.urls import path, re_path
from .views import *

urlpatterns = [
    path("", producto, name='producto'),
    path("crear/", producto_store, name='producto_crear'),
    re_path(r"editar/(?P<pk>\d+)/$", producto_update, name='producto_editar'),
    re_path(r"eliminar/(?P<pk>\d+)/$", producto_destroy, name='producto_eliminar'),
    re_path(r"(?P<pk>\d+)/$", producto_detalle, name='producto_detalle'),
    path("marcas/", marca, name='marca'),
    path("marcas/crear/", marca_store, name='marca_crear'),
    re_path(r"marcas/editar/(?P<pk>\d+)/$", marca_update, name='marca_editar'),
    re_path(r"marcas/eliminar/(?P<pk>\d+)/$", marca_destroy, name='marca_eliminar'),
    path("categorias/", categoria, name="categoria"),
    path("categorias/crear/", categoria_store, name="categoria_crear"),
    re_path(r"categoras/editar/(?P<pk>\d+)/$", categoria_update, name='categoria_editar'),
    re_path(r"categoras/eliminar/(?P<pk>\d+)/$", categoria_destroy, name='categoria_eliminar'),   
]
