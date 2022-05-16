from datetime import datetime, timedelta

from django.db.models import Sum


def sum_total_conta(model, field):
    """
    Agregado do valor das Entradas ou Saídas
    """
    return model.objects.filter(conta=field).aggregate(valor_total=Sum('valor'))


def sum_parcelas(parcelas):
    """
    Soma das contas parceladas
    """
    soma = 0
    for p in parcelas:
        if p.parcela > 1:
            soma_parcela = p.valor / p.parcela
            soma += soma_parcela
    return soma


def sum_faturas(faturas):
    """
    Soma dos pagamentos pelo filtro
    """
    fatura = 0
    for f in faturas:
        if f.tipo == "Pagamento Fatura":
            fatura += f.valor
    return fatura


def is_valid(model):
    """
    Valida se o valor total não é None
    """
    if model.get('valor_total') is not None:
        return True
    else:
        return False


def is_valid_saida(saida, conta):
    """
    Subtrai o valor total da conta
    """
    if is_valid(saida):
        conta.valor -= saida.get('valor_total')
    else:
        conta.valor = conta.valor
    return conta.valor


def is_valid_entrada(entrada, conta):
    """
    Soma o valor total da conta
    """
    if is_valid(entrada):
        conta.valor += entrada.get('valor_total')
    else:
        conta.valor = conta.valor
    return conta.valor


def filter_by_conta(model, field):
    """
    Filtro dos Logs por conta
    """
    return model.filter(conta=field)


def filter_by_else(model, field):
    """
    Else do filtro dos Logs por conta
    """
    return model.objects.filter(conta=field)


def filter_by_model_date(model, month, year):
    """
    Fitro por Model para data/mês
    """
    return model.objects.filter(data__month=month, data__year=year)


def check_final_date(data, parcela):
    """
    Retorna a data da parcela final
    """
    return data + timedelta(seconds=parcela * 30 * 24 * 60 * 60)