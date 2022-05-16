from django.contrib import admin

# Register your models here.
from controle.models import *


class ListBancos(admin.ModelAdmin):
    list_display = ('id', 'nome')
    list_display_links = ('id', 'nome')


class ListContas(admin.ModelAdmin):
    list_display = ('id', 'tipo', 'limite', 'limite_usado', 'limite_restante', 'valor', 'banco')
    list_display_links = ('id', 'tipo')
    list_filter = ('tipo', 'banco',)
    list_editable = ('limite', 'valor', )


class ListEntradas(admin.ModelAdmin):
    list_display = ('id', 'nome', 'tipo', 'valor', 'data', 'conta')
    list_display_links = ('id', 'nome',)
    list_filter = ('tipo', 'data', 'conta',)
    list_editable = ('data', 'valor', 'tipo',)

class ListSaidas(admin.ModelAdmin):
    list_display = ('id', 'nome', 'tipo', 'parcela', 'valor', 'data', 'conta')
    list_display_links = ('id', 'nome',)
    list_filter = ('tipo', 'data', 'conta',)
    list_editable = ('data', 'valor', 'tipo', 'parcela', )


admin.site.register(Banco, ListBancos)
admin.site.register(Conta, ListContas)
admin.site.register(Entrada, ListEntradas)
admin.site.register(Saida, ListSaidas)
