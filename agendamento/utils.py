import requests
import xmltodict
import calendar
from candidato.models import Candidato
from django.utils import timezone
from datetime import datetime
from .models import Agendamento
from candidato.utils import string_to_date, carregar_informacoes


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
    

def buscar_dia_semana(data):
    dias_semana = ['Segunda-Feira', 'Terça-Feira', ' Quarta-Feira', 'Quinta-Feira', 'Sexta-Feira', 'Sabádo', 'Domingo']
    dia = data.weekday()
    return dias_semana[dia]


def expirou_horario(data, hora):
    if data < timezone.now().date():
        return 'Sim'
    elif data == timezone.now().date():
        hora = datetime.strptime(hora, "%H:%M").time()
        if hora > datetime.now().time():
            return 'Sim'
        else:
            return 'Não'
    else:
        return 'Não'


def carregar_agendamentos(usuario):

    dados = []

    id = usuario.id
    candidato = Candidato.objects.get(id=id)
    lista_agendamentos = candidato.agendamentos.all()


    for agendamento in lista_agendamentos:
        dados.append({
            'cnes': agendamento.estabelecimento.cnes,
            'estabelecimento': agendamento.estabelecimento.nome,
            'dia_semana': buscar_dia_semana(agendamento.horario.data),
            'data': agendamento.horario.data.strftime("%d/%m/%Y"),
            'hora': datetime.strptime(agendamento.horario.horas,"%H").time(),
            'passou_hora': expirou_horario(agendamento.horario.data, agendamento.horario.horas)
        })
    
    return dados


def disponibilidade_estabelecimento(estabelecimento, usuario):

    try:
        estabelecimentos = Agendamento.objects.filter(estabelecimento_id=estabelecimento)
    except Exception as e:
        # Tratamento de exceção, se necessário
        print(f"Erro ao buscar agendamentos: {e}")
        return []
    
    candidato = carregar_informacoes(usuario)
    hora = hora_por_idade(candidato['idade'])

    datas_indisponiveis = []
    for agendamento in estabelecimentos:
        horario = agendamento.horario
        if horario.horas == hora:
            if horario.vagas == 0:
                datas_indisponiveis.append(horario.data)
    
    ano_atual = datetime.now().year
    mes_atual = datetime.now().month
    #Range de agendamento de 2 meses
    mes_seguinte = mes_atual + 1
    datas = obter_dias_quarta_a_sabado(ano_atual, mes_atual) + obter_dias_quarta_a_sabado(ano_atual, mes_seguinte)

    for data in datas:
        str_data = data
        data = string_to_date(data)
        if data in datas_indisponiveis:
            
            datas.remove(str_data)
    return datas


def obter_dias_quarta_a_sabado(ano, mes):
    # Retorna uma matriz de listas onde cada lista representa uma semana do mês
    semanas = calendar.monthcalendar(ano, mes)
    datas = []
    # Itera sobre cada semana do mês
    for semana in semanas:
        # Itera sobre cada dia da semana
        for dia in semana:
            # Se o dia estiver dentro do mês, imprima a data
            if dia != 0:
                data = f'{ano}-{mes:02d}-{dia:02d}'
                if not verifica_data(string_to_date(data)):
                    datas.append(data)
    
    return datas
