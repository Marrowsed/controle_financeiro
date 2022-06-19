from django.shortcuts import render

from controle.models import *


def list_accounts_chart(request):
    conta = Conta.objects.all()

    data = {
        'conta': conta
    }

    return render(request, 'chart/list_chart.html', data)

def account_chart(request, pk):
    conta = Conta.objects.get(id=pk)


    data = {
        'conta': conta
    }

    return render(request, 'chart/account_chart.html', data)