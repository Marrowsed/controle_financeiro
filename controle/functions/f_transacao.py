from django.contrib import messages
from django.db.models import F
from django.shortcuts import redirect

from controle.models import *


def get_error_message_corrente(type, message):
    list_types = ['Compra Parcelada']
    var = [i for i in list_types if i in type]
    if var:
        messages.error(request, message, extra_tags="alert alert-danger")
        return redirect('adiciona_saida')
    else:
        return False


def get_error_message_poupanca(type, message):
    list_types = ['Transferência']
    var = [i for i in list_types if i not in type]
    if var:
        messages.error(request, message, extra_tags="alert alert-danger")
        return redirect('adiciona_saida')
    else:
        return False


def get_error_message_credito(type, message):
    list_types = ['Pagamento Fatura', 'Transferência', 'Poupança']
    var = [i for i in list_types if i in type]
    if var:
        messages.error(request, message, extra_tags="alert alert-danger")
        return redirect('adiciona_saida')
    else:
        return False


def get_error_message_limite(message):
    return messages.error(request, message, extra_tags="alert alert-danger")


def validate_decrease_limite(model, value):
    validate = model.limite - value
    if validate > 0:
        return True
    else:
        get_error_message_limite("Valor Ultrapassou o limite !")
        return redirect('index')


def validate_decrease_value(model, value):
    validate = model.valor - value
    if validate > 0:
        return True
    else:
        get_error_message_limite("Valor Ultrapassou o limite !")
        return redirect('index')

def create_object_saida(name, type, parcela, final_value, date, account):
    saida = Saida.objects.create(nome=name, tipo=type, parcela=parcela,
                                 valor=final_value, data=date,
                                 conta=account)
    return saida.save()


def actions_credito(tipo, model, value, nome, parcela, data):
    get_error_message_credito(tipo, "Tipo não permitido !")
    valor = float(value)
    validate_decrease_limite(model, valor)
    model.limite_usado = F('limite_usado') + valor
    model.limite_restante = F('limite') - F('limite_usado')
    model.save()
    create_object_saida(nome, tipo, parcela, value, data, model)


def actions_poupanca(tipo, model, value, nome, parcela, data):
    get_error_message_poupanca(tipo, "Tipo não permitido !")
    validate_decrease_value(model, value)
    model.valor = F('valor') - value
    model.save()
    create_object_saida(nome, tipo, parcela, value, data, model)

def actions_corrente(tipo, model, value, nome, parcela, data):
    get_error_message_poupanca(tipo, "Tipo não permitido !")
    validate_decrease_value(model, value)
    model.valor = F('valor') - value
    model.save()
    create_object_saida(nome, tipo, parcela, value, data, model)
