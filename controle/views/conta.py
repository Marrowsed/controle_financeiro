from django.shortcuts import render, redirect
from django.contrib import messages

from controle.models import *
from controle.functions import *


def index(request):
    conta = Conta.objects.all().order_by('banco')
    data = {
        'conta': conta
    }
    return render(request, 'index.html', data)


def conta(request, pk):
    pesquisa = f"{datetime.now().year}-{datetime.now().month:02}"
    conta = Conta.objects.get(id=pk)
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
        list_parcelado = check_is_parcelado(Saida, conta, ano, mes)

        data.update({
            'parcela': list_parcelado
        })
        soma_saida = sum_saida(data_saida, list_parcelado, data_saida)
        soma_entrada = sum_faturas(data_entrada)
        soma_fatura = soma_saida - soma_entrada
        data.update({
            'saida': data_saida, 'fatura': soma_fatura, 'entrada': data_entrada
        })
        '''
        saida = sum_total_conta(Saida, conta)
        entrada = sum_total_conta(Entrada, conta)
        if conta.tipo != "Crédito":
            is_valid_saida(saida, conta)
            is_valid_entrada(entrada, conta)
        else:
            if is_valid(saida):
                conta.limite_usado += saida.get('valor_total')
                conta.limite_restante = (conta.limite - conta.limite_usado) - soma_fatura
            else:
                conta.limite_usado = conta.limite_usado
                conta.limite_restante = conta.limite_restante
            '''

    return render(request, 'conta/conta.html', data)


def add_conta(request):
    banco = Banco.objects.all()
    data = {
        'banco': banco
    }
    if request.method == 'POST':
        tipo = request.POST['tipo']
        limite = request.POST['limite']
        valor = request.POST['valor']
        banco = request.POST['banco']
        if Conta.objects.filter(tipo=tipo, banco=banco):
            messages.error(request, "Conta já existente !", extra_tags="alert alert-danger")
        else:
            b = Banco.objects.get(id=banco)
            conta = Conta.objects.create(tipo=tipo, limite=limite, limite_usado=0, limite_restante=limite,
                                         valor=valor, banco=b)
            conta.save()
            return redirect('index')
    return render(request, 'conta/add_conta.html', data)


def edita_conta(request, pk):
    conta = Conta.objects.get(id=pk)
    if request.method == 'POST':
        if conta.tipo == "Crédito":
            conta.limite = float(request.POST['limite'])
        else:
            conta.valor = request.POST['valor']
        conta.save()
        return redirect('index')
    data = {
        'conta': conta
    }
    return render(request, 'conta/edita_conta.html', data)


def deleta_conta(request, pk):
    conta = Conta.objects.get(id=pk)
    conta.delete()
    return redirect('index')


def list_contas(request):
    conta = Conta.objects.all().order_by('banco')
    data = {
        'conta': conta
    }
    return render(request, 'conta/list_contas.html', data)
