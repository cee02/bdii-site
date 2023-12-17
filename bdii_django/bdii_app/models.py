from django.db import models
from django.contrib.auth.models import AbstractUser

class Armazem(models.Model):
    id_armazem = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)  # Assuming nome is the name of the component
    descricao = models.TextField()  # Assuming descricao is the description
    quantidade_em_stock = models.IntegerField()
    data_entrada = models.DateTimeField(auto_now_add=True)
    data_saida = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'armazem'

    def __str__(self):
        return f"{self.nome} - Quantidade em Stock: {self.quantidade_em_stock}"

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    endereco = models.CharField(max_length=255)
    telefone = models.CharField(max_length=15)
    email = models.EmailField()
    contribuinte = models.CharField(max_length=20)

    class Meta:
        db_table = 'cliente'

    def __str__(self):
        return f"{self.nome} - {self.endereco} - {self.telefone} - {self.email} - {self.contribuinte}"
      
        

        