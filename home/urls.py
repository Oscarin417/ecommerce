from django.urls import path
from .views import *

urlpatterns = [
    path("", home, name='home'),
    path("login/", sigin, name='sigin'),
    path("registro/", register, name='registro'),
    path("sinout/", sinout, name='sinout'),
    path("configuracion/", configuracion, name='config'),
    path("mis_compras/", compras, name='compras'),
    path("carrito/", carrito, name='carrito'),
]
