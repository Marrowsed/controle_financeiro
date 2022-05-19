from django.db.models import F

from controle.models import *


def get_account(account):
    return Conta.objects.get(id=account)


def is_savings(account):
    return account.tipo == "Poupança"


def validate_increase_limite(account, value):
    limite = account.limite
    valor = float(value)
    validate = limite + valor
    if validate <= limite:
        return True
    else:
        return False


def create_object_saida(name, type, parcela, final_value, date, account):
    """
    Cria o objeto Saída
    """
    saida = Saida.objects.create(nome=name, tipo=type, parcela=parcela,
                                 valor=final_value, data=date,
                                 conta=account)
    return saida.save()


def create_object_entrada(name, type, final_value, date, account):
    """
    Cria o objeto Entrada
    """
    entrada = Entrada.objects.create(nome=name, tipo=type, valor=final_value,
                                     data=date, conta=account)
    return entrada.save()


def send_to_account(to_account, account, value, name, parcela, type, date):
    conta = get_account(to_account)
    if not is_savings(conta):
        account.valor = F('valor') - value
        conta.valor = F('valor') + value
        create_object_saida(name, type, parcela, value, date, account)
        create_object_entrada(name, type, value, date, conta)
        account.save()
        conta.save()


def apply_savings(savings, account, value, name, parcela, type, date):
    poupanca = get_account(savings)
    if is_savings(poupanca):
        account.valor = F('valor') - value
        poupanca.valor = F('valor') + value
        create_object_saida(name, type, parcela, value, date, account)
        create_object_entrada(name, type, value, date, poupanca)
        account.save()
        poupanca.save()


def pay_fatura(to_account, account, value, name, parcela, type, date):
    conta = get_account(to_account)
    if not is_savings(conta):
        if validate_increase_limite(conta, value):
            account.valor = F('valor') - value
            conta.limite = F('limite') + value
            create_object_saida(name, type, parcela, value, date, account)
            create_object_entrada(name, type, value, date, conta)
            account.save()
            conta.save()
