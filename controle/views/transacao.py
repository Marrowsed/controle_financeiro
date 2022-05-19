from django.db.models import F
from django.shortcuts import render, redirect

from controle.functions import *


def add_entrada(request, pk):
    conta = Conta.objects.get(id=pk)

    if request.method == 'POST':
        nome = request.POST['nome']
        tipo = request.POST['tipo']
        valor_final = request.POST['valor']
        data = request.POST['data']
        tipo_conta = request.POST['conta']
        if get_saida_error_message(tipo, tipo_conta):
            messages.error(request, "Tipo de Operação não Permitida !", extra_tags="alert alert-danger")
        elif tipo_conta == "Crédito":
            actions_credito(tipo, conta, valor_final, nome, data)
        elif tipo_conta == "Poupança":
            actions_poupanca(tipo, conta, valor_final, nome, data)
        elif tipo_conta == "Corrente":
            actions_corrente(tipo, conta, valor_final, nome, data)
        return redirect('index')

    data = {
        'conta': conta
    }

    return render(request, 'index.html', data)


def add_saida(request, pk):
    conta = Conta.objects.get(id=pk)

    if request.method == 'POST':
        print(conta.valor)
        nome = request.POST['nome']
        tipo = request.POST['tipo']
        parcela = request.POST['parcela']
        valor_final = request.POST['valor']
        data = request.POST['data']
        tipo_conta = request.POST['conta']
        if get_saida_error_message(tipo, tipo_conta):
            messages.error(request, "Tipo de Operação não Permitida !", extra_tags="alert alert-danger")
        else:
            if tipo_conta == "Crédito" and validate_decrease_limite(conta, valor_final):
                actions_credito(tipo, conta, valor_final, nome, parcela, data)
                return redirect('index')
            elif tipo_conta == "Poupança" and validate_decrease_value(conta, valor_final):
                actions_poupanca(tipo, conta, valor_final, nome, parcela, data)
                return redirect('index')
            elif tipo_conta == "Corrente" and validate_decrease_value(conta, valor_final):
                actions_corrente(tipo, conta, valor_final, nome, parcela, data)
                return redirect('index')
            else:
                messages.error(request, "Valor Ultrapassou o limite !", extra_tags="alert alert-danger")

    data = {
        'conta': conta
    }

    return render(request, 'transacao/add_saida.html', data)
