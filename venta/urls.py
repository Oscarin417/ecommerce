from django.urls import path
from .views import *

urlpatterns = [
    path("crear/", venta_store, name='venta_crear'),
    path("crear/paypal/", pago_paypal, name='paypal'),
    path("crear/openpay/", pago_openpay, name='openpay'),
    path("webhook/openpay/", openpay_webhook, name='openpay_webhook'),
    path("carrito/agregar/", carrito_agregar, name='carrito_agregar'),
    path("carrito/eliminar/", carrito_eliminar, name='carrito_eliminar'),
]
