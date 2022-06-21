from django.shortcuts import render
from datetime import datetime

from controle.models import *


def list_accounts_chart(request):
    conta = Conta.objects.all()

    data = {
        'conta': conta
    }

    return render(request, 'chart/list_chart.html', data)

def account_chart(request, pk):
    conta = Conta.objects.get(id=pk)
    entries = Entrada.objects.filter(conta=conta.id, data__year=datetime.now().year, data__month=datetime.now().month)
    minus = Saida.objects.filter(conta=conta.id, data__year=datetime.now().year, data__month=datetime.now().month)
    search = f"{datetime.now().year}-{datetime.now().month:02}"
    sum_entries = 0
    sum_minus = 0
    for e in entries:
        sum_entries += e.valor
    for m in minus:
        sum_minus += m.valor
    data = {
        'conta': conta, 'search': search, 'sum_entries': sum_entries, 'sum_minus': sum_minus
    }

    if request.GET.get('periodo'):
        search = request.GET.get('periodo')
        y, m = search.split("-")
        month_entries = Entrada.objects.filter(conta=conta, data__year=y, data__month=m)
        month_minus = Saida.objects.filter(conta=conta, data__year=y, data__month=m)
        for e in month_entries:
            sum_entries += e.valor
        for m in month_minus:
            sum_minus += m.valor
        data.update({
            'sum_entries': int(sum_entries), 'sum_minus': int(sum_minus), 'search': search
        })

    return render(request, 'chart/account_chart.html', data)