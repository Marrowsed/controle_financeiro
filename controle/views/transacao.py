from django.db.models import F
from django.contrib import messages
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
        final_data = str(data)
        actual_data = str(datetime.now())
        if get_entrada_error_message(tipo, tipo_conta):
            messages.error(request, "Tipo de Operação não Permitida !", extra_tags="alert alert-danger")
        elif tipo_conta == "Crédito":
            actions_credito_entrada(tipo, conta, valor_final, nome, data)
        elif tipo_conta == "Poupança":
            if datetime.fromisoformat(final_data) >= datetime.fromisoformat(actual_data):
                messages.info(request, "Operação Agendada !", extra_tags="alert alert-info")
            actions_poupanca_entrada(tipo, conta, valor_final, nome, data)
        elif tipo_conta == "Corrente":
            if datetime.fromisoformat(final_data) >= datetime.fromisoformat(actual_data):
                messages.info(request, "Operação Agendada !", extra_tags="alert alert-info")
            actions_corrente_entrada(tipo, conta, valor_final, nome, data)
        return redirect('index')

    data = {
        'conta': conta, 'contas': contas
    }

    return render(request, 'transacao/add_entrada.html', data)


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
        final_data = str(data)
        actual_data = str(datetime.now())
        if get_saida_error_message(tipo, tipo_conta):
            messages.error(request, "Tipo de Operação não Permitida !", extra_tags="alert alert-danger")
        else:
            if tipo_conta == "Crédito" and validate_decrease_limite(conta, valor_final):
                actions_credito_saida(tipo, conta, valor_final, nome, parcela, data)
                return redirect('index')
            elif tipo_conta == "Poupança" and validate_decrease_value(conta, valor_final):
                if datetime.fromisoformat(final_data) >= datetime.fromisoformat(actual_data):
                    messages.info(request, "Operação Agendada !", extra_tags="alert alert-info")
                actions_poupanca_saida(tipo, conta, valor_final, nome, parcela, data)
                return redirect('index')
            elif tipo_conta == "Corrente" and validate_decrease_value(conta, valor_final):
                if datetime.fromisoformat(final_data) >= datetime.fromisoformat(actual_data):
                    messages.info(request, "Operação Agendada !", extra_tags="alert alert-info")
                conta_destino = request.POST['conta_destino']
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


def show_saida(request, pk, id):
    conta = Conta.objects.get(id=pk)
    saida = Saida.objects.get(id=id)

    if request.method == "POST":
        saida.nome = request.POST['nome']
        saida.tipo = request.POST['tipo']
        saida.parcela = request.POST['parcela']
        saida.valor = request.POST['valor']
        saida.save()
    data = {
        'conta': conta, 'saida': saida
    }

    return render(request, 'transacao/show_movimento.html', data)


def show_entrada(request, pk, id):
    conta = Conta.objects.get(id=pk)
    entrada = Entrada.objects.get(id=id)

    if request.method == "POST":
        entrada.nome = request.POST['nome']
        entrada.tipo = request.POST['tipo']
        entrada.valor = request.POST['valor']
        entrada.save()
    data = {
        'conta': conta, 'entrada': entrada
    }

    return render(request, 'transacao/show_movimento.html', data)


def delete_saida(request, pk, id):
    conta = Conta.objects.get(id=pk)
    saida = Saida.objects.get(id=id)
    action_delete_saida(conta, saida)


def delete_entrada(request, pk, id):
    conta = Conta.objects.get(id=pk)
    entrada = Entrada.objects.get(id=id)
    action_delete_entrada(conta, entrada)
