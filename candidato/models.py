from django.db import models
from django.contrib.auth.models import User

class GrupoAtendimento(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self) -> str:
        return str(self.nome) 

class Candidato(User):
    nome = models.CharField(max_length=120)
    data_nascimento = models.DateField()
    grupo_atendimento = models.ManyToManyField(GrupoAtendimento, blank=True)
    covid = models.BooleanField(default=False)

    def __str__(self) -> str:
        return str(self.nome)
