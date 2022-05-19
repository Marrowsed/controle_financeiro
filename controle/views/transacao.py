from django.db.models import F
from django.shortcuts import render, redirect

from controle.functions import *


def add_entrada(request, pk):
    conta = Conta.objects.get(id=pk)

    data = {
        'conta': conta
    }

    return render(request, 'index.html', data)


def add_saida(request, pk):
    conta = Conta.objects.get(id=pk)
    saida = Saida.objects.all()

    if request.method == 'POST':
        nome = request.POST['nome']
        tipo = request.POST['tipo']
        parcela = request.POST['parcela']
        valor_final = request.POST['valor']
        data = request.POST['data']
        tipo_conta = request.POST['conta']
        if tipo_conta == "Crédito":
            if get_error_message_credito(tipo):
                messages.error(request, "Tipo de Operação não Permitida !", extra_tags="alert alert-danger")
            else:
                actions_credito(tipo, conta, valor_final, nome, parcela, data)
                return redirect('index')
        elif tipo_conta == "Poupança":
            if get_error_message_poupanca(tipo):
                messages.error(request, "Tipo de Operação não Permitida !", extra_tags="alert alert-danger")
            else:
                actions_poupanca(tipo, conta, valor_final, nome, parcela, data)
                return redirect('index')
        elif tipo_conta == "Corrente":
            if get_error_message_corrente(tipo):
                messages.error(request, "Tipo de Operação não Permitida !", extra_tags="alert alert-danger")
            else:
                actions_corrente(tipo, conta, valor_final, nome, parcela, data)
                return redirect('index')

    data = {
        'conta': conta, 'saida': saida
    }

    return render(request, 'transacao/add_saida.html', data)
