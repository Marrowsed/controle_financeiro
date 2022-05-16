from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="index"),
    path('conta/<str:pk>', conta, name="conta"),
    path('conta/<str:pk>/edita', edita_conta, name="edita_conta"),
    path('conta/<str:pk>/deleta', deleta_conta, name="edita_conta"),
    path('conta/<str:pk>/entrada', add_entrada, name="adiciona_entrada"),
    path('conta/<str:pk>/saida', add_saida, name="adiciona_saida"),


]