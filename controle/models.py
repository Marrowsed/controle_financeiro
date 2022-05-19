from django.db import models

from datetime import datetime


class Banco(models.Model):
    nome = models.CharField(max_length=200)
    foto = models.ImageField(upload_to="banco", blank=True)

    def __str__(self):
        return self.nome


class Conta(models.Model):
    TIPO = (
        ('Poupança', 'Poupança'),
        ('Crédito', 'Crédito'),
        ('Corrente', 'Corrente')
    )
    tipo = models.CharField(max_length=200, choices=TIPO)
    limite = models.FloatField(default=0)
    limite_usado = models.FloatField(default=0)
    limite_restante = models.FloatField(default=0)
    valor = models.FloatField(default=0)
    banco = models.ForeignKey(Banco, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.tipo == "Crédito":
            self.limite_restante = self.limite - self.limite_usado
        super(Conta, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.banco} - {self.tipo}"


class Entrada(models.Model):
    TIPO = (
        ('Salário', 'Salário'),
        ('Transferência', 'Transferência'),
        ('Pagamento Fatura', 'Pagamento Fatura'),
        ('Outros', 'Outros')
    )
    nome = models.CharField(max_length=200)
    tipo = models.CharField(max_length=200, choices=TIPO)
    valor = models.FloatField()
    data = models.DateField(default=datetime.today)
    conta = models.ForeignKey(Conta, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome


class Saida(models.Model):
    TIPO = (
        ('Compra', 'Compra'),
        ('Compra Parcelada', 'Compra Parcelada'),
        ('Pagamento Fatura', 'Pagamento Fatura'),
        ('Transferência', 'Transferência'),
        ('Poupança', 'Poupança'),
        ('Outros', 'Outros')
    )
    nome = models.CharField(max_length=200)
    tipo = models.CharField(max_length=200, choices=TIPO)
    parcela = models.IntegerField()
    valor = models.FloatField()
    data = models.DateField(default=datetime.today)
    conta = models.ForeignKey(Conta, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

'''
class Extrato(models.Model):
    TIPO = (
        ('Entrada', 'Entrada'),
        ('Saida', 'Saida')
    )
    conta = models.ForeignKey(Conta, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=200, choices=TIPO)
    entrada = models.ForeignKey(Entrada, on_delete=models.CASCADE, blank=True, null=True)
    saida = models.ForeignKey(Saida, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.conta} - {self.tipo}"
'''