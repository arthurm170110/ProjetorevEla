import requests
import xmltodict
from django.utils import timezone
from datetime import datetime

from .models import Candidato


def string_to_date(data):
    return datetime.strptime(data, "%Y-%m-%d").date()


def calcular_idade(data_nascimento):
    return (timezone.now().date() - data_nascimento).days // 365

def carregar_grupos_atendimento():
    
    url = "https://selecoes.lais.huol.ufrn.br/media/grupos_atendimento.xml"

    response = requests.get(url)
    try:
        data = xmltodict.parse(response.content)
    except:
        print("Failed to parse xml from response")
    
    return data


def apto(data_nascimento, covid, grupo_atendimento):
    data_nascimento = string_to_date(data_nascimento)
    idade = calcular_idade(data_nascimento)
    if idade < 18:
        return  'Você não está apto para participar da pesquisa.'  
    if covid == 'True':
        return 'Você não está apto para participar da pesquisa.'
    
    for grupo in grupo_atendimento:
        if grupo == (70) or grupo == (65) or grupo == (67):
           return 'Você não está apto para participar da pesquisa.'
        
    return 'Você está apto para participar da pesquisa.'


def carregar_informacoes(candidato):
        
    id = candidato.id

    usuario = Candidato.objects.get(id=id)
    
    grupoAtendimento = []

    nome = usuario.nome
    data_nascimeto = usuario.data_nascimento
    idade = calcular_idade(data_nascimeto)
    cpf = candidato.username

    for grupo in usuario.grupo_atendimento.all():
        grupoAtendimento.append(grupo.id)
        
    apitidao = apto(data_nascimeto.strftime("%Y-%m-%d"), str(usuario.covid), grupoAtendimento)

    if "não" in apitidao:
        apitidao = False
    else:
        apitidao = True

    informacoes = {
        "nome": nome,
        "data_nascimento": data_nascimeto,
        "idade": idade,
        "cpf": cpf,
        "apto": apitidao
    }

    return informacoes
