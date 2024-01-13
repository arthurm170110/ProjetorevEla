from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from candidato.utils import carregar_informacoes
from .utils import *
from django.http import HttpResponse

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

                    return HttpResponse("Agendamento realizado com sucesso!")
                else:
                    return HttpResponse("As vagas já foram todas preenchidas")
