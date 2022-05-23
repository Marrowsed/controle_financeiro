from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="index"),
    path('bancos', list_bancos, name="bancos"),
    path('bancos/adicionar', add_banco, name="adiciona_banco"),
    path('banco/<str:pk>/edita', edita_banco, name="edita_banco"),
    path('banco/<str:pk>/deleta', deleta_banco, name="deleta_banco"),
    path('conta/<str:pk>', conta, name="conta"),
    path('conta/<str:pk>/edita', edita_conta, name="edita_conta"),
    path('conta/<str:pk>/deleta', deleta_conta, name="deleta_conta"),
    path('conta/<str:pk>/entrada', add_entrada, name="adiciona_entrada"),
    path('conta/<str:pk>/entrada/<str:id>', show_entrada, name="mostra_entrada"),
    path('conta/<str:pk>/entrada/<str:id>/deleta', delete_entrada, name="deleta_entrada"),
    path('conta/<str:pk>/saida', add_saida, name="adiciona_saida"),
    path('conta/<str:pk>/saida/<str:id>', show_saida, name="mostra_saida"),
    path('conta/<str:pk>/saida/<str:id>/deleta', delete_saida, name="deleta_saida"),
    path('contas', list_contas, name="contas"),
    path('contas/adicionar', add_conta, name="adiciona_conta"),



]