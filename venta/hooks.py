from django.dispatch import receiver
from paypal.standard.models import ST_PP_COMPLETED, ST_PP_CANCELED_REVERSAL
from paypal.standard.ipn.signals import valid_ipn_received
from .models import Venta
from ecommerce.settings import PAYPAL_RECEIVER_EMAIL
from datetime import datetime

@receiver(valid_ipn_received)
def paypal_status(sender, **kwargs):
    ipn_obj = sender
    print(ipn_obj)
    ventas = Venta.objects.filter(estatus='P', pasarela_id=1, fecha_creacion=ipn_obj.invoice)
    for venta in ventas:
        if ipn_obj.payment_status == ST_PP_COMPLETED and ipn_obj.receiver_email == PAYPAL_RECEIVER_EMAIL:
            print("Pago completado")
            producto = venta.producto
            venta.estatus = 'S'
            venta.fecha_creacion = datetime.now()
            venta.save()
            producto.cantidad -= venta.cantidad
            producto.save()
        elif ipn_obj.payment_status == ST_PP_CANCELED_REVERSAL and ipn_obj.receiver_email == PAYPAL_RECEIVER_EMAIL:
            print("Pago cancelado")
            venta.estatus = 'C'
            venta.save()
