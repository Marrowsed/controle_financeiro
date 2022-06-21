from django.shortcuts import redirect

from controle.functions.f_between import *

def check_schedule(data):
    """
    Checa se é um agendamento
    """
    final_data = str(data)
    actual_data = str(datetime.now())
    if datetime.fromisoformat(final_data) >= datetime.fromisoformat(actual_data):
        return True
    else:
        return False

def get_account_credito(model):
    """
    Retorna se a conta é do tipo Crédito
    """
    return model.tipo == "Crédito"


def get_validate_error(list_type, action_type):
    """
    Valida se a lista de ações do tipo de conta são válidas !
    """
    if not [i for i in list_type if i in action_type]:
        return True
    else:
        return False


# FUNCTIONS FOR SAÍDA
def get_saida_error_message(action_type, account_type):
    """
    Retorna se as ações são válidas ou não
    """
    if account_type == "Crédito":
        list_types = ['Compra Parcelada']
        var = get_validate_error(list_types, action_type)
        return var
    elif account_type == "Poupança":
        list_types = ['Transferência']
        var = get_validate_error(list_types, action_type)
        return var
    elif account_type == "Corrente":
        list_types = ['Compra', 'Pagamento Fatura', 'Transferência', 'Poupança', 'Outros', 'Agendamento']
        var = get_validate_error(list_types, action_type)
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

def create_object_saida_schedule(name, parcela, final_value, date, account):
    """
    Cria o objeto Saída Agendado
    """
    saida = Saida.objects.create(nome=name, tipo="Agendamento", parcela=parcela,
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
            if check_schedule(data):
                valor = float(value)
                create_object_saida_schedule(nome, parcela, valor, data, model)
            else:
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



# FUNCTIONS FOR ENTRADA

def create_object_entrada(name, type, final_value, date, account):
    """
    Cria o objeto Entrada
    """
    entrada = Entrada.objects.create(nome=name, tipo=type, valor=final_value,
                                     data=date, conta=account)
    return entrada.save()

def create_object_entrada_schedule(name, final_value, date, account):
    """
    Cria o objeto Entrada Agendado
    """
    entrada = Entrada.objects.create(nome=name, tipo="Agendamento", valor=final_value,
                                     data=date, conta=account)
    return entrada.save()


def get_entrada_error_message(action_type, account_type):
    """
    Retorna se as ações são válidas ou não
    """
    if account_type == "Crédito":
        list_types = ['Pagamento Fatura']
        var = get_validate_error(list_types, action_type)
        return var
    elif account_type == "Poupança":
        list_types = ['Poupança']
        var = get_validate_error(list_types, action_type)
        return var
    elif account_type == "Corrente":
        list_types = ['Salário', 'Transferência', 'Outros', "Agendamento"]
        var = get_validate_error(list_types, action_type)
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
    if check_schedule(data):
        valor = float(value)
        create_object_entrada_schedule(nome, valor, data, model)
    else:
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

