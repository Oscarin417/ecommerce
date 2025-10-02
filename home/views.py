import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from usuario.forms import RegistroForm, DomicilioForm
from usuario.models import Domicilio, Usuario
from producto.models import Producto
from utils.open_pay import Open_Pay
from venta.models import Venta

# Create your views here.
def home(request):
    usuario = request.user
    productos = Producto.objects.all()
    context = {
        'productos': productos,
    }
    if request.user.is_authenticated:
        if usuario.rol == 3:
            return render(request, 'index.html', context)
        else:
            return render(request, 'admin.html')
    else:
        return render(request, 'index.html', context)

def sigin(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            print("No se encontro al usuario")
    return render(request, 'login.html')

def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = RegistroForm(request.POST or None)
    context = {'form': form}
    if request.method=='POST':
        try:
            if form.is_valid():
                f = form.save(commit=False)
                f.password = make_password(request.POST['password'])
                f.domicilio = Domicilio.objects.create()
                f.rol = 3
                f.save()
                login(request, f)
                return redirect('home')
            else:
                print(form.errors)
        except Exception as e:
            print(f"error: {e}")
    return render(request, 'registro.html', context)

@login_required
def sinout(request):
    logout(request)
    return redirect('home')

@login_required
def configuracion(request):
    usuario = get_object_or_404(Usuario, username=request.user)
    domicilio = usuario.domicilio
    form = DomicilioForm(request.POST or None, instance=domicilio)
    op = Open_Pay()
    context = {'form': form}
    if request.method == 'POST':
        try:
            if form.is_valid():
                form.save()
                u = op.create_client(user=usuario, domicilio=form)
                usuario.atributos = json.dumps(u)
                usuario.save()
                return redirect('home')
            else:
                print(form.errors)
        except Exception as e:
            print(f"error: {e}")
    return render(request, 'configuracion.html', context)

@login_required
def compras(request):
    ventas = Venta.objects.filter(usuario=request.user)
    context = {'ventas': ventas}
    return render(request, 'compra.html', context)

@login_required
def carrito(request):
    return render(request, 'carrito.html')
