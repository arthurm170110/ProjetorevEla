from django.shortcuts import render
from rest_framework import generics

import requests
from xml.etree import ElementTree

from .models import Candidato, GrupoAtendimento
from .serializers import CandidatoSerializer, GrupoAtendimentoSerializer

def carregar_grupos_atendimento():
    url_xml = 'https://selecoes.lais.huol.ufrn.br/media/grupos_atendimento.xml'
    response = requests.get(url_xml)

    if response.status_code == 200:
        root = ElementTree.fromstring(response.text)

        for grupo_element in root.findall('grupoatendimento'):
            nome_grupo = grupo_element.find('nome').text
            _, created = GrupoAtendimento.objects.get_or_create(nome = nome_grupo)



class CandidatoListCreateView(generics.ListCreateAPIView):

    carregar_grupos_atendimento()

    queryset = Candidato.objects.all()
    serializer_class = CandidatoSerializer


class GrupoAtendimentoListView(generics.ListAPIView):
    queryset = GrupoAtendimento.objects.all()
    serializer_class = GrupoAtendimentoSerializer
