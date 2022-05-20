from django.shortcuts import redirect

from controle.functions.f_between import *


def get_account_credito(model):
    """
    Retorna se a conta é do tipo Crédito
    """
    return model.tipo == "Crédito"


# FUNCTIONS FOR SAÍDA
def get_validate_error_saida(list, type):
    """
    Valida se a lista de ações do tipo de conta são válidas !
    """
    if not [i for i in list if i in type]:
        return True
    else:
        return False


def get_saida_error_message(type, account_type):
    """
    Retorna se as ações são válidas ou não
    """
    if account_type == "Crédito":
        list_types = ['Compra Parcelada']
        var = get_validate_error_saida(list_types, type)
        return var
    elif account_type == "Poupança":
        list_types = ['Transferência']
        var = get_validate_error_saida(list_types, type)
        return var
    elif account_type == "Corrente":
        list_types = ['Compra', 'Pagamento Fatura', 'Transferência', 'Poupança', 'Outros']
        var = get_validate_error_saida(list_types, type)
        return var


def validate_decrease_limite(model, value):
    """
    Valida se ultrapassou o limite da conta
    """
    valor = float(value)
    validate = model.limite_restante - valor
    if validate > 0:
        return True
    else:
        return False


def validate_decrease_value(model, value):
    """
    Valida se ultrapassou o valor da conta
    """
    valor = float(value)
    validate = model.valor - valor
    if validate > 0:
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


def actions_credito_saida(tipo, model, value, nome, parcela, data):
    """
    Ações na Conta tipo Crédito
    """
    valor = float(value)
    model.limite_usado = F('limite_usado') + valor
    model.limite_restante = F('limite') - F('limite_usado')
    model.save()
    create_object_saida(nome, tipo, parcela, value, data, model)


def actions_poupanca_saida(tipo, model, value, nome, parcela, data):
    """
    Ações na Conta tipo Poupança
    """
    valor = float(value)
    model.valor = F('valor') - valor
    model.save()
    create_object_saida(nome, tipo, parcela, valor, data, model)


def actions_corrente_saida(tipo, model, value, nome, parcela, data, conta_destino):
    """
    Ações na Conta tipo Corrente
    """
    if tipo == "Poupança":
        apply_savings(conta_destino, model, value, nome, parcela, tipo, data)
    elif tipo == "Transferência":
        send_to_account(conta_destino, model, value, nome, parcela, tipo, data)
    elif tipo == "Pagamento Fatura":
        pay_fatura(conta_destino, model, value, nome, parcela, tipo, data)
    else:
        if conta_destino == "":
            valor = float(value)
            model.valor = F('valor') - valor
            model.save()
            create_object_saida(nome, tipo, parcela, valor, data, model)
        else:
            return False
    return True


def action_delete_saida(model, saida):
    """
    Ação para deletar uma saída
    """
    if get_account_credito(model):
        valor_final = model
        valor_final.limite_usado = F('limite_usado') - saida.valor
        valor_final.save()
    else:
        valor_final = model
        valor_final.valor = F('valor') + saida.valor
        valor_final.save()
    saida.delete()
    return redirect('index')


# FUNCTIONS FOR ENTRADA

def create_object_entrada(name, type, final_value, date, account):
    """
    Cria o objeto Entrada
    """
    entrada = Entrada.objects.create(nome=name, tipo=type, valor=final_value,
                                     data=date, conta=account)
    return entrada.save()


def get_validate_error_entrada(list, type):
    """
    Valida se a lista de ações do tipo de conta são válidas !
    """
    if not [i for i in list if i in type]:
        return True
    else:
        return False


def get_entrada_error_message(type, account_type):
    """
    Retorna se as ações são válidas ou não
    """
    if account_type == "Crédito":
        list_types = ['Pagamento Fatura']
        var = get_validate_error_saida(list_types, type)
        return var
    elif account_type == "Poupança":
        list_types = ['Transferência']
        var = get_validate_error_saida(list_types, type)
        return var
    elif account_type == "Corrente":
        list_types = ['Salário', 'Transferência', 'Outros']
        var = get_validate_error_saida(list_types, type)
        return var


def actions_credito_entrada(tipo, model, value, nome, data):
    """
    Ações na Conta tipo Crédito
    """
    valor = float(value)
    model.limite_usado = F('limite_usado') - valor
    model.limite_restante = F('limite') - F('limite_usado')
    model.save()
    create_object_entrada(nome, tipo, value, data, model)


def actions_poupanca_entrada(tipo, model, value, nome, data):
    """
    Ações na Conta tipo Poupança
    """
    valor = float(value)
    model.valor = F('valor') + valor
    model.save()
    create_object_entrada(nome, tipo, valor, data, model)


def actions_corrente_entrada(tipo, model, value, nome, data):
    """
    Ações na Conta tipo Corrente
    """
    valor = float(value)
    model.valor = F('valor') + valor
    model.save()
    create_object_entrada(nome, tipo, valor, data, model)


def action_delete_entrada(model, entrada):
    """
    Ação para deletar uma entrada
    """
    if get_account_credito(model):
        valor_final = model
        valor_final.limite_usado = F('limite_usado') + entrada.valor
        valor_final.save()
    else:
        valor_final = model
        valor_final.valor = F('valor') - entrada.valor
        valor_final.save()
    entrada.delete()
    return redirect('index')
