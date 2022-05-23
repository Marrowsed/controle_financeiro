from django.shortcuts import render
from django.contrib import messages

from controle.models import *


def list_bancos(request):
    banco = Banco.objects.all()


    data = {
        'banco': banco
    }
    return render(request, 'banco/list_bancos.html', data)

def edita_banco(request, pk):
    banco = Banco.objects.get(id=pk)

    if request.method == "POST":
        nome = request.POST['nome']
        imagem = request.FILES['imagem']
        banco.save(nome=nome, foto=imagem)
    data = {
        'banco': banco
    }
    return render(request, 'banco/edita_banco.html', data)


def deleta_banco(request, pk):
    banco = Banco.objects.get(id=pk)
    banco.delete()


def add_banco(request):
    if request.method == "POST":
        nome = request.POST['nome']
        foto = request.FILES['foto']
        if Banco.objects.filter(nome__icontains=nome):
            messages.info(request, "Banco já existente", extra_tags="alert alert-danger")
        else:
            banco = Banco.objects.create(nome=nome, foto=foto)
            banco.save(nome=nome, foto=foto)
            return 'index'
    return render(request, 'banco/add_banco.html')
