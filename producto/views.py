from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *

# Create your views here.
@login_required
def marca(request):
    marcas = Marca.objects.all()
    context = {'marcas': marcas}
    return render(request, 'marca/list.html', context)

@login_required
@transaction.atomic
def marca_store(request):
    form = MarcaForm(request.POST or None)
    context = {
        'form': form,
        'marca': False,
    }

    if request.method == 'POST':
        try:
            if form.is_valid():
                form.save()
                return redirect('marca')
            else:
                print(form.errors)
        except Exception as e:
            print(f"error: {e}")
    return render(request, 'marca/form.html', context)

@login_required
@transaction.atomic
def marca_update(request, pk):
    marca = get_object_or_404(Marca, pk=pk)
    form = MarcaForm(request.POST or None, instance=marca)
    context = {
        'form': form,
        'marca': True,
    }

    if request.method == 'POST':
        try:
            if form.is_valid():
                form.save()
                return redirect('marca')
            else:
                print(form.errors)
        except Exception as e:
            print(f"error: {e}")
    return render(request, 'marca/form.html', context)

@login_required
@transaction.atomic
def marca_destroy(request, pk):
    marca = get_object_or_404(Marca, pk=pk)

    if request.method == 'POST':
        marca.delete()
        return redirect('marca')

@login_required
def categoria(request):
    categorias = Categoria.objects.all()
    context = {'categorias': categorias}
    return render(request, "categoria/list.html", context)

@login_required
@transaction.atomic
def categoria_store(request):
    form = CategoriaForm(request.POST or None)
    context = {
        'form': form,
        'categoria': False,
    }

    if request.method == 'POST':
        try:
            if form.is_valid():
                form.save()
                return redirect('categoria')
            else:
                print(form.errors)
        except Exception as e:
            print(f"error: {e}")
    return render(request, 'categoria/form.html', context)

@login_required
@transaction.atomic
def categoria_update(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    form = CategoriaForm(request.POST or None, instance=categoria)
    context = {
        'form': form,
        'categoria': True
    }

    if request.method == 'POST':
        try:
            if form.is_valid():
                form.save()
                return redirect('categoria')
            else:
                print(form.errors)
        except Exception as e:
            print(f"error: {e}")
    return render(request, 'categoria/form.html', context)

@login_required
@transaction.atomic
def categoria_destroy(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)

    if request.method == 'POST':
        categoria.delete()
        return redirect('categoria')

@login_required
def producto(request):
    productos = Producto.objects.all()
    context = {'productos': productos}

    return render(request, 'producto/list.html', context)

@login_required
@transaction.atomic
def producto_store(request):
    form = ProductoForm(request.POST or None, request.FILES or None)
    context = {
        'form': form,
        'producto': False,
    }

    if request.method == 'POST':
        try:
            if form.is_valid():
                form.save()
                return redirect('producto')
            else:
                print(form.errors)
        except Exception as e:
            print(f"error: {e}")
    return render(request, 'producto/form.html', context)

@login_required
@transaction.atomic
def producto_update(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    form = ProductoForm(request.POST or None, request.FILES or None, instance=producto)
    context = {
        'form': form,
        'producto': True,
    }

    if request.method == 'POST':
        try:
            if form.is_valid():
                form.save()
                return redirect('producto')
            else:
                print(form.errors)
        except Exception as e:
            print(f"error: {e}")
    return render(request, 'producto/form.html', context)

@login_required
@transaction.atomic
def producto_destroy(request, pk):
    producto = get_object_or_404(Producto, pk=pk)

    if request.method == 'POST':
        producto.delete()
        return redirect('producto')
    else:
        return redirect('home')

def producto_detalle(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    cantidad = range(1, producto.cantidad +1)
    context = {'producto': producto,
               'cantidad': cantidad}
    return render(request, 'producto/detalle.html', context)
