import requests
import xmltodict
from django.utils import timezone
from datetime import datetime


def carregar_grupos_atendimento():
    # import ipdb
    url = "https://selecoes.lais.huol.ufrn.br/media/grupos_atendimento.xml"

    response = requests.get(url)
    try:
        data = xmltodict.parse(response.content)
    except:
        print("Failed to parse xml from response")
    # ipdb.set_trace()
    return data


def apto(data_nascimento, covid, grupo_atendimento):
    data_nascimento = datetime.strptime(data_nascimento, "%Y-%m-%d").date()
    idade = (timezone.now().date() - data_nascimento).days // 365
    if idade < 18:
        return  'Você não está apto para participar da pesquisa.'  
    if covid == 'True':
        return 'Você não está apto para participar da pesquisa.'
    
    for grupo in grupo_atendimento:
        if grupo == (70) or grupo == (65) or grupo == (67):
           return 'Você não está apto para participar da pesquisa.'
        
    return 'Você está apto para participar da pesquisa.'

