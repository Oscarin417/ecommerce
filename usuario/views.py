import json
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import *
from .forms import *
from utils.open_pay import Open_Pay

# Create your views here.
@login_required
def domicilio(request):
    domicilios = Domicilio.objects.all()
    context = {'domicilios': domicilios}

    return render(request, 'domicilio.html', context)

@login_required
def usuario(request):
    usuarios = Usuario.objects.all()
    context = {'usuarios': usuarios}

    return render(request, 'list.html', context)

@login_required
@transaction.atomic
def usuario_store(request):
    uf = UsuarioForm(request.POST or None)
    df = DomicilioForm(request.POST or None)
    context = {'df': df,
               'uf': uf}
    op = Open_Pay()

    if request.method == 'POST':
        try:
            if df.is_valid() and uf.is_valid():
                f = uf.save(commit=False)
                f.domicilio = df.save()
                u = op.create_client(user=f, domicilio=df)
                f.password = make_password(request.POST['password'])
                f.atributos = json.dumps(u)
                f.save()
                return redirect('usuario')
            else:
                print(df.errors)
                print(uf.errors)
        except Exception as e:
            print(f"error: {e}")
    return render(request, 'create.html', context)

@login_required
@transaction.atomic
def usuario_update(request, pk):
    usuario = Usuario.objects.get(pk=pk)
    domicilio = usuario.domicilio
    uf = UsuarioForm(request.POST or None, instance=usuario)
    df = DomicilioForm(request.POST or None, instance=domicilio)
    context = {'df': df,
               'uf': uf}

    if request.method == 'POST':
        try:
            if df.is_valid() and uf.is_valid():
                f = uf.save(commit=False)
                f.password = make_password(request.POST['password'])
                f.save()
                df.save()
                return redirect('usuario')
            else:
                print(df.errors)
                print(uf.errors)
        except Exception as e:
            print(f"error: {e}")
    return render(request, 'edit.html', context)

@login_required
@transaction.atomic
def usuario_destroy(request, pk):
    usuario = Usuario.objects.get(pk=pk)
    domicilio = usuario.domicilio

    if request.method == 'POST':
        domicilio.delete()
        usuario.delete()
        return redirect('usuario')

@login_required
def perfil(request):
    usuario = Usuario.objects.get(pk=request.user.id)
    form = PerfilForm(request.POST or None, instance=usuario)
    context = {'form': form}

    if request.method == 'POST':
        try:
            if form.is_valid():
                form.save()
                return redirect('home')
            else:
                print(form.errors)
        except Exception as e:
            print(f'error: {e}')
    return render(request, 'perfil.html', context)
