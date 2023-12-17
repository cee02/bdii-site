from django.db import models
from django.contrib.auth.models import AbstractUser

class Componente(models.Model):
    username = models.CharField(max_length=255)
    quantidade_em_stock = models.IntegerField()

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    endereco = models.CharField(max_length=255)
    telefone = models.CharField(max_length=20)
    email = models.EmailField()
    contribuinte = models.CharField(max_length=20)

    class Meta:
        db_table = 'cliente'

    def __str__(self):
        return f"{self.nome} - {self.endereco} - {self.telefone} - {self.email} - {self.contribuinte}"
      
        

        