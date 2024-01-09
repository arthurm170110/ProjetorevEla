from rest_framework import serializers

from .models import Candidato, GrupoAtendimento
from .validators import cpf_valido


class GrupoAtendimentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrupoAtendimento
        fields = '__all__'


class CandidatoSerializer(serializers.ModelSerializer):
    grupos_atendimento = GrupoAtendimentoSerializer(many = True, read_only = True)

    class Meta:
        model = Candidato
        fields = '__all__'

    def validate(self, data):
        cpf_valido(data['cpf'])
        return data