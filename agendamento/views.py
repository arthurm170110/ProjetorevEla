from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from candidato.utils import carregar_informacoes
from .utils import *
from django.http import JsonResponse
from .models import Agendamento, Horario, Estabelecimento
from candidato.models import Candidato 
from candidato.utils import string_to_date


@login_required
def cadastro_agendamento(request):
    estabelecimentos = carregar_estabelecimentos()
    usuario = request.user
    informacoes = carregar_informacoes(usuario)
    lista_estabelecimento = estabelecimentos['estabelecimentos']['estabelecimento']

    if request.method == "GET":
        for estab in lista_estabelecimento:
            nome = estab['no_fantasia']
            cnes = estab['co_cnes']
            
            Estabelecimento.objects.get_or_create(nome=nome, cnes=cnes)
        dados = {
            'estabelecimentos': lista_estabelecimento,
            'apto': informacoes['apto']
        }
        return render(request, 'agendamento.html', dados)
    
    if request.method == "POST":

        if verifica_agendamento(usuario):
            dados = {"mensagem_erro": 'Você possui um agendamento ativo.', 
                     "apto": informacoes['apto'],
                     "nome": informacoes['nome'],
                     "data_nascimento": informacoes['data_nascimento'],
                     "idade": informacoes['idade'],
                     "cpf": informacoes['cpf']
                    }
            return render(request, 'candidato_logado.html',dados)

        else:
            co_cnes = request.POST.get('estabelecimento')
            data = request.POST.get('data')

            data = string_to_date(data)
            if verifica_data(data):
                return render(request, 'agendamento.html', {"data_invalida": verifica_data(data), "estabelecimentos": lista_estabelecimento, "apto": informacoes['apto']})

            else:
                for estab in lista_estabelecimento:
                    nome = estab['no_fantasia']
                    cnes = estab['co_cnes']
                    
                    Estabelecimento.objects.get_or_create(nome=nome, cnes=cnes) 

                hora = hora_por_idade(informacoes['idade'])
                horario, _ = Horario.objects.get_or_create(horas=hora, data=data)

                if horario.vagas > 0:
                    horario.vagas = horario.vagas - 1
                    horario.save()
                    estabelecimento = Estabelecimento.objects.get(cnes=co_cnes)
                    candidato = Candidato.objects.get(id=usuario.id)

                    Agendamento.objects.create(

                        estabelecimento = estabelecimento,
                        candidato = candidato,
                        horario = horario
                    )

                    dados = {
                        "mensagem_sucesso": 'Agendamento realizado com sucesso!',
                        "apto": informacoes['apto'],
                        "agendamentos": carregar_agendamentos(usuario)

                    }

                    return render(request, 'list_agendamentos.html', dados)
                else:
                    return render(request, 'agendamento.html', {"mensagem_erro": 'As vagas já foram todas preenchidas', "estabelecimentos": lista_estabelecimento, "apto": informacoes['apto']})
                

@login_required
def lista_agendamento(request):
    
    usuario = request.user
    informacoes = carregar_informacoes(usuario)
    agendamentos = carregar_agendamentos(usuario)

    dados = {
        "apto": informacoes['apto'],
        "agendamentos": agendamentos    
    }

    if len(agendamentos) == 0:
        dados["mensagem_erro"] = "Você não possui agendamentos."

    return render(request, 'list_agendamentos.html', dados)


@login_required
def carregar_datas_disponiveis_view(request, estabelecimento):
    estab = Estabelecimento.objects.get(cnes=estabelecimento)
    datas_disponiveis = disponibilidade_estabelecimento(estab.id, request.user)

    response_data = {'datas_disponiveis': datas_disponiveis}
    return JsonResponse(response_data)


@login_required
def obter_hora_view(request):
    usuario = request.user
    informacoes = carregar_informacoes(usuario)
    hora = hora_por_idade(informacoes['idade'])

    return JsonResponse({"hora": hora})