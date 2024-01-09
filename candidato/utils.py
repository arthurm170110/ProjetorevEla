import requests
import xmltodict
from django.utils import timezone


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


def apto(cantidato):
    idade = (timezone.now().date() - cantidato.data_nascimento).days // 365

    if idade < 18:
        return  {'O candidato não está apto para participar da pesquisa.'}   
    if cantidato.covid:
        return {'O candidato não está apto para participar da pesquisa.'}
    
    for grupos in cantidato.grupo_atendimento.all():
        if grupos.id == (70) or grupos.id == (65) or grupos.id == (67):
           return {'O candidato não está apto para participar da pesquisa.'} 
        
    return {'O candidato está apto para participar da pesquisa.'}

