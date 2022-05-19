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


def sum_parcela_final(lista):
    soma = 0
    for l in lista:
        parcela = int(l.parcela.split('/')[-1])
        if parcela > 1:
            soma_parcela = l.valor / parcela
            soma += soma_parcela
    return soma

def sum_saida_geral(saida):
    """
    Soma das Saidas
    """
    soma = 0
    for s in saida:
        if s.tipo != "Compra Parcelada":
            soma += s.valor
    return soma


def sum_saida(parcelas, lista, saida):
    """
    Soma dos pagamentos pelo filtro Saída + Parcelados
    """
    parcela = sum_parcelas(parcelas)
    parcela_final = sum_parcela_final(lista)
    saida = sum_saida_geral(saida)
    return parcela + parcela_final + saida


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


def filter_by_model_conta(model, field):
    """
    Filtro por Model e conta
    """
    return model.objects.filter(conta=field)


def filter_by_model_date_conta(model, month, year, field):
    """
    Fitro por Model para data/mês e conta
    """
    return model.objects.filter(data__month=month, data__year=year, conta=field)


def replace_month_year(data, month, year):
    """
    Encapsulamento da função replace
    """
    return data.replace(month=int(month), year=int(year))


def check_final_date(data, parcela):
    """
    Retorna a data da parcela final
    """
    return data + timedelta(seconds=(parcela-1) * 30 * 24 * 60 * 60)


def check_is_parcelado(model, field, year, month):
    """
    Retorna uma lista que será exibida as compras parceladas !
    """
    compra_saida = filter_by_model_conta(model, field)
    list_saida = []
    for c in compra_saida:
        if get_date_iso_format(year, month) >= c.data:
            list_saida.append(c)
            data_final = check_final_date(c.data, c.parcela)
            parcela = (int(month) - c.data.month)
            if data_final > replace_month_year(get_date_iso_format(year, month), month, year):
                if parcela > 0:
                    c.parcela = f"{parcela + 1}/{c.parcela}"
                else:
                    c.parcela = f"{parcela + 12}/{c.parcela}"
                c.data = replace_month_year(c.data, month, year)
            elif data_final < replace_month_year(get_date_iso_format(year, month), month, year):
                list_saida.remove(c)
    return list_saida


def get_date_iso_format(year, month):
    """
    Retorna uma data em String year/month/01
    """
    return datetime.fromisoformat(f"{year}-{month}-01").date()
