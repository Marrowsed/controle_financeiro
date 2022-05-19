from django.db.models import F
from django.shortcuts import render, redirect

from controle.functions import *


def add_entrada(request, pk):
    conta = Conta.objects.get(id=pk)
    contas = Conta.objects.filter(banco=conta.banco)

    if request.method == 'POST':
        nome = request.POST['nome']
        tipo = request.POST['tipo']
        valor_final = request.POST['valor']
        data = request.POST['data']
        tipo_conta = request.POST['conta']
        conta_destino = request.POST['conta_destino']
        if get_saida_error_message(tipo, tipo_conta):
            messages.error(request, "Tipo de Operação não Permitida !", extra_tags="alert alert-danger")
        elif tipo_conta == "Crédito":
            actions_credito_saida(tipo, conta, valor_final, nome, data)
        elif tipo_conta == "Poupança":
            actions_poupanca_saida(tipo, conta, valor_final, nome, data)
        elif tipo_conta == "Corrente":
            actions_corrente_saida(tipo, conta, valor_final, nome, data)
        return redirect('index')

    data = {
        'conta': conta, 'contas': contas
    }

    return render(request, 'index.html', data)


def add_saida(request, pk):
    conta = Conta.objects.get(id=pk)
    contas = Conta.objects.all().order_by('banco')

    if request.method == 'POST':
        nome = request.POST['nome']
        tipo = request.POST['tipo']
        parcela = request.POST['parcela']
        valor_final = request.POST['valor']
        data = request.POST['data']
        tipo_conta = request.POST['conta']
        conta_destino = request.POST['conta_destino']
        if get_saida_error_message(tipo, tipo_conta):
            messages.error(request, "Tipo de Operação não Permitida !", extra_tags="alert alert-danger")
        else:
            if tipo_conta == "Crédito" and validate_decrease_limite(conta, valor_final):
                actions_credito_saida(tipo, conta, valor_final, nome, parcela, data)
                return redirect('index')
            elif tipo_conta == "Poupança" and validate_decrease_value(conta, valor_final):
                actions_poupanca_saida(tipo, conta, valor_final, nome, parcela, data)
                return redirect('index')
            elif tipo_conta == "Corrente" and validate_decrease_value(conta, valor_final):
                a = actions_corrente_saida(tipo, conta, valor_final, nome, parcela, data, conta_destino)
                if a:
                    return redirect('index')
                else:
                    messages.error(request, "Operação não permitida !", extra_tags="alert alert-danger")
            else:
                messages.error(request, "Valor Ultrapassou o limite !", extra_tags="alert alert-danger")

    data = {
        'conta': conta, 'contas': contas
    }

    return render(request, 'transacao/add_saida.html', data)
