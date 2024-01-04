from rest_framework import serializers
from .models import Candidato, GrupoAtendimento


class GrupoAtendimentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrupoAtendimento
        fields = '__all__'


class CandidatoSerializer(serializers.ModelSerializer):
    grupos_atendimento = GrupoAtendimentoSerializer(many = True, read_only = True)

    class Meta:
        model = Candidato
        fields = '__all__'