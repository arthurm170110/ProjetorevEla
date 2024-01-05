from django.db import models

class GrupoAtendimento(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self) -> str:
        return str(self.nome) 

class Candidato(models.Model):
    nome = models.CharField(max_length=120)
    cpf = models.CharField(max_length=15, unique=True)
    data_nascimento = models.DateField()
    grupo_atendimento = models.ManyToManyField(GrupoAtendimento, blank=True)
    covid = models.BooleanField()
    senha = models.CharField(max_length=255)
