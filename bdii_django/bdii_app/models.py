from django.db import models
from django.contrib.auth.models import AbstractUser

class Componente(models.Model):
    username = models.CharField(max_length=255)
    quantidade_em_stock = models.IntegerField()

class CustomUser(AbstractUser):
    # Adicione campos personalizados, se necessário
    pass

class Aluno(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    # Adicione campos adicionais, se necessário
    perfil = models.CharField(max_length=10, choices=[('aluno_a', 'Aluno A'), ('aluno_b', 'Aluno B'), ('aluno_c', 'Aluno C')])

    def __str__(self):
        return f"{self.user.username} - {self.perfil}"
    
CustomUser._meta.get_field('groups').remote_field.related_name = 'customuser_groups'
CustomUser._meta.get_field('user_permissions').remote_field.related_name = 'customuser_user_permissions'
        