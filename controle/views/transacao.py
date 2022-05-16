from django.shortcuts import render

from controle.models import *


def add_entrada(request, pk):
    conta = Conta.objects.get(id=pk)


    data = {
        'conta': conta
    }

    return render(request, 'index.html', data)

def add_saida(request, pk):
    conta = Conta.objects.get(id=pk)


    data = {
        'conta': conta
    }

    return render(request, 'index.html', data)