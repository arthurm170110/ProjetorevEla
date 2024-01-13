from django.db import models

from candidato.models import Candidato

HORAS_DISPONIVEIS = [('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'), ('17', '17')]


class Estabelecimento(models.Model):
    nome = models.CharField(max_length=120)
    cnes = models.CharField(max_length=10)

    def __str__(self) -> str:
        return str(self.nome)
    

class Horario(models.Model):
    vagas = models.IntegerField(default=5)
    data = models.DateField()
    horas = models.CharField(max_length=5, choices=HORAS_DISPONIVEIS)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['data', 'horas'], name='data_hora')
        ]

    def __str__(self) -> str:
        return str(self.vagas) + str(self.data) + str(self.horas)
    

class Agendamento(models.Model):
    estabelecimento = models.ForeignKey(Estabelecimento, on_delete=models.CASCADE)
    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE, related_name='agendamentos')
    ativo = models.BooleanField(default=True)
    horario = models.ForeignKey(Horario, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.estabelecimento) + str(self.candidato) + str(self.ativo) + str(self.horario)
