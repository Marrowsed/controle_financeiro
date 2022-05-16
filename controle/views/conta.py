from django.shortcuts import render, redirect

from controle.models import *
from controle.functions import *


def index(request):
    conta = Conta.objects.all()
    data = {
        'conta': conta
    }
    return render(request, 'index.html', data)


def conta(request, pk):
    pesquisa = f"{datetime.now().year} - {datetime.now().month:02}"
    conta = Conta.objects.get(id=pk)
    saida = sum_total_conta(Saida, conta)
    entrada = sum_total_conta(Entrada, conta)
    data = {
        'pesquisa': pesquisa, 'conta': conta
    }
    if request.GET.get('mes'):
        pesquisa = request.GET.get('mes')
        ano, mes = pesquisa.split('-')
        data.update({
            'pesquisa': pesquisa
        })
        data_saida = filter_by_model_date_conta(Saida, mes, ano, conta)
        data_entrada = filter_by_model_date_conta(Entrada, mes, ano, conta)
        soma = sum_parcelas(data_saida)
        fatura = sum_faturas(data_entrada)
        soma -= fatura
        data.update({
            'saida': data_saida, 'fatura': soma, 'entrada': data_entrada
        })
        if conta.tipo != "Crédito":
            is_valid_saida(saida, conta)
            is_valid_entrada(entrada, conta)
        else:
            if is_valid(saida):
                conta.limite_usado += saida.get('valor_total')
                conta.limite_restante = conta.limite - conta.limite_usado
            else:
                conta.limite_usado = conta.limite_usado
                conta.limite_restante = conta.limite_restante
        # data.update({
        #   'despesa': saida
        # })

    return render(request, 'conta/conta.html', data)


def edita_conta(request, pk):
    conta = Conta.objects.get(id=pk)
    data = {
        'conta': conta
    }
    return render(request, 'index.html', data)


def deleta_conta(request, pk):
    conta = Conta.objects.get(id=pk)
    conta.delete()
    return redirect('index')
