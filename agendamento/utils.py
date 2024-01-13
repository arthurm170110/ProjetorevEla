import requests
import xmltodict

from candidato.models import Candidato
from django.utils import timezone


def carregar_estabelecimentos():
    url = "https://selecoes.lais.huol.ufrn.br/media/estabelecimentos_pr.xml"

    response = requests.get(url)
    try:
        data = xmltodict.parse(response.content)
    except:
        print("Failed to parse xml from response")
    return data


def verifica_agendamento(usuario):
    id = usuario.id
    candidato = Candidato.objects.get(id=id)
    agendamento_ativo = candidato.agendamentos.filter(ativo=True).first()
    
    if agendamento_ativo:
        data = agendamento_ativo.horario.data
        if data < timezone.now().date():
            agendamento_ativo.ativo = False
            agendamento_ativo.save()
            return False
        else:
            return True
    return False
    

def hora_por_idade(idade):
    if idade >= 18 and idade <= 29:
        return '13'
    elif idade >= 30 and idade <= 39:
        return '14'
    elif idade >= 40 and idade <= 49:
        return '15'
    elif idade >= 50 and idade <= 59:
        return '16'
    elif idade >= 60:
        return '17'
    

def verifica_data(data):
    if not (2 <= data.weekday() <= 5):
        return 'Esta data não está entre Quarta e Sábado!'
    if data < timezone.now().date():
        return 'Só é possível agendamento de datas futuras.'
