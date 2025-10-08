from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json, os
from producto.models import Producto
from paypal.standard.forms import PayPalPaymentsForm
from .models import Venta
from utils.open_pay import Open_Pay
from datetime import datetime
from ecommerce.settings import PAYPAL_RECEIVER_EMAIL

# Create your views here.
@csrf_exempt
def openpay_webhook(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        description = data.get('transaction', {}).get('description', '')
        descripciones = description.split(", ")
        print(f"descripciones: {descripciones}")

        if data.get('transaction', {}).get('status', '') == 'completed':
            try:
                for d in descripciones:
                    producto = get_object_or_404(Producto, nombre=d)
                    venta = get_object_or_404(Venta, pasarela_id=2, estatus='P', producto=producto)
                    venta.estatus = 'S'
                    venta.atributos = json.dumps(data)
                    venta.fecha_creacion = datetime.now()
                    venta.save()
                    producto.cantidad -= venta.cantidad
                    producto.save()
                return HttpResponse('Pago completado', status=200)
            except Exception as e:
                print(f'error: {e}')
                return HttpResponse(f'error: {e}', status=500)
        return HttpResponse('Webhook recibido con éxito', status=200)

@login_required
def venta_store(request):
    if request.method == 'POST':
        ids = request.POST.getlist('id')
        cantidades = request.POST.getlist('cantidad')
        nombres = request.POST.getlist('nombre')
        context = {
            'ids': ids,
            'cantidades': cantidades,
            'nombres': nombres,
        }
        return render(request, 'menu.html', context)
    else:
        return redirect('home')

@login_required
def pago_paypal(request):
    fecha = datetime.now()
    if request.method == 'POST':
        data = {
            'ids': request.POST.getlist('id'),
            'cantidades': request.POST.getlist('cantidad'),
            'nombres': request.POST.getlist('nombre'),
        }
        print(data)
        total_final = 0
        for producto_id, cantidad in zip(data['ids'], data['cantidades']):
            product = get_object_or_404(Producto, pk=int(producto_id))
            total = float(product.precio * int(cantidad))
            print(f"total: {total}")
            total_final += total
            print(f"total_final: {total_final}")
            Venta.objects.create(
                usuario = request.user,
                producto = product,
                cantidad = int(cantidad),
                fecha_creacion = fecha,
                total = total,
                pasarela_id = 1
            )
        paypal_dict = {
            "business": PAYPAL_RECEIVER_EMAIL,
            "amount": f"{total_final:.2f}",
            "item_name": '',
            "invoice": fecha,
            "currency_code": "MXN",
            "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
            "return": request.build_absolute_uri(reverse('home')),
            "cancel_return": request.build_absolute_uri(reverse('home')),
        }
        if len(data['nombres']) == 1 :
            paypal_dict['item_name'] = data['nombres'][0]
        else:
            paypal_dict['item_name'] = 'compra de articulos'
        request.session['productos'] = {}
        request.session['cantidad_carrito'] = 0
        form = PayPalPaymentsForm(initial=paypal_dict)
        context = {'form': form}
        return render(request, 'paypal.html', context)
    else:
        return redirect('home')

@login_required
def pago_openpay(request):
    usuario = request.user
    atributos = json.loads(usuario.atributos) if usuario.atributos else {}
    op = Open_Pay()
    if not atributos:
        u = op.create_client(user=usuario, domicilio=usuario.domicilio)
        usuario.atributos = json.dumps(u)
        usuario.save()
    if request.method == 'POST':
        pago = {}
        total_final = 0
        ventas = []
        efectivo = {}
        nombres = ''
        ids = request.POST.getlist('id')
        cantidades = request.POST.getlist('cantidad')
        nombres = request.POST.getlist('nombre')
        print(request.POST)
        if isinstance(nombres, list) and isinstance(cantidades, list) and isinstance(ids, list):
            print("se recibieron listas")
            for producto_id, cantidad in zip(ids, cantidades):
                product = get_object_or_404(Producto, pk=int(producto_id))
                total = float(product.precio * int(cantidad))
                total_final += total
                venta = Venta.objects.create(
                    usuario = usuario,
                    producto = product,
                    cantidad = int(cantidad),
                    total = total,
                    pasarela_id = 2,
                    atributos = {},
                    fecha_creacion = datetime.now()
                )
                ventas.append(venta)
            nombres_productos = ''
            for venta in ventas:
                nombres_productos = ', '.join(nombres)
            efectivo = op.pago_referencia(cliente_id=atributos.get('id', ''), monto=total_final, concepto=nombres_productos)
            for venta in ventas:
                venta.atributos = json.dumps(efectivo)
                venta.save()
            pago = json.loads(ventas[0].atributos)
        else:
            print("No se recibieron listas")
            producto_id = request.POST['id']
            cantidad = request.POST['cantidad']
            nombres = request.POST['nombre']
            product = get_object_or_404(Producto, pk=int(producto_id))
            total = float(product.precio * int(cantidad))
            total_final += total
            nombre = request.POST['nombre']
            print(f"nombre: {nombre}")
            efectivo = op.pago_referencia(cliente_id=atributos.get('id', ''), monto=total_final, concepto=nombre)
            venta = Venta.objects.create(
                usuario = usuario,
                producto = product,
                cantidad = int(cantidad),
                total = total,
                pasarela_id = 2,
                atributos = json.dumps(efectivo),
                fecha_creacion = datetime.now()
            )
            pago = json.loads(venta.atributos)

        request.session['productos'] = {}
        request.session['cantidad_carrito'] = 0
        context = {
            'pago_id': pago.get('payment_method', {}).get('reference', ''),
            'id': os.environ.get('OPENPAY_ID'),
        }
        return render(request, 'openpay.html', context)
    else:
        return redirect('home')


def carrito_agregar(request):
    if request.method == 'POST':
        producto_id = int(request.POST.get('id'))
        cantidad = int(request.POST.get('cantidad'))
        producto = get_object_or_404(Producto, pk=producto_id)
        diccionario = request.session.get('productos', {})
        if producto.nombre in diccionario:
            diccionario[producto.nombre]['cantidad'] += cantidad
        else:
            diccionario[producto.nombre] = {
                'id': producto_id,
                'nombre': producto.nombre,
                'cantidad': cantidad,
            }
            cantidad_carrito = len(diccionario)
            request.session['cantidad_carrito'] = cantidad_carrito
        request.session['productos'] = diccionario
        request.session.modified = True
        return redirect('carrito')
    else:
        return redirect('home')

def carrito_eliminar(request):
    diccionario = request.session.get('productos', {})
    if request.method == 'POST':
        producto = request.POST.get('nombre', '')
        del diccionario[producto]
        request.session['productos'] = diccionario
        request.session['cantidad_carrito'] -= 1
        request.session.modified = True
        return JsonResponse({'status': 'ok'})
    else:
        return redirect('home')
