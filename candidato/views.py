from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .funcoes import carregar_grupos_atendimento, apto

from .models import Candidato, GrupoAtendimento
from .serializers import CandidatoSerializer, GrupoAtendimentoSerializer


class CandidatoListCreateView(APIView):
    def get(self, request):
        queryset = Candidato.objects.all()
        serializer_class = CandidatoSerializer(queryset, many=True)
        return Response(serializer_class.data)
    
    def post(self, request):
        serializer = CandidatoSerializer(data=request.data)
        if serializer.is_valid():

            dicionario = carregar_grupos_atendimento()
            grupos = dicionario['grupos']['grupoatendimento']

            for grupo in grupos:
                nome = grupo['nome']
                _, created = GrupoAtendimento.objects.get_or_create(nome=nome)

            serializer.save()

            cantidato = Candidato.objects.last()
            resposta = apto(cantidato)

            dados = {
                'Registro': serializer.data,
                'Aptidao': resposta
            }

            return Response(dados, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GrupoAtendimentoListView(generics.ListAPIView):

    queryset = GrupoAtendimento.objects.all()
    serializer_class = GrupoAtendimentoSerializer
