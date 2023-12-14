from django.db import models

class Componente(models.Model):
    nome = models.CharField(max_length=255)
    quantidade_em_stock = models.IntegerField()

    def __str__(self):
        return self.nome