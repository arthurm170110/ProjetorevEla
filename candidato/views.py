from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .utils import carregar_grupos_atendimento, apto, calcular_idade
from .validators import cadastro_valido

from .models import Candidato, GrupoAtendimento


def paginainicial(request):
    if request.method == "GET":
        if not request.user.is_authenticated:
            return render(request, 'paginainicial.html')
        return redirect('perfil')


def candidatos(request):
    if request.method == "GET":
        dicionario = carregar_grupos_atendimento()
        grupos = dicionario['grupos']
        return render(request, 'candidato.html', grupos)
    
    elif request.method == "POST":
        nome = request.POST.get('nome')
        cpf = request.POST.get('cpf')
        data_nascimento = request.POST.get('data_nascimento')
        covid = request.POST.get('covid')
        grupo_atendimento_str = request.POST.getlist('grupo_atendimento')
        grupo_atendimento = [int(valor) for valor in grupo_atendimento_str]
        senha = request.POST.get('senha')
        confirma_senha = request.POST.get('confirma_senha')

        validacao = cadastro_valido(cpf, data_nascimento, senha, confirma_senha)


        if validacao:
            dicionario = carregar_grupos_atendimento()
            grupos = dicionario['grupos']['grupoatendimento']
            dados = {
                "mensagens_de_erro": validacao,
                "grupoatendimento": grupos,
                "campos": {
                    'nome': nome,
                    'cpf': cpf,
                    'data_nascimento': data_nascimento,
                    'covid': covid,
                    'grupoAtendimento': grupo_atendimento_str,
                }
            }
            return render(request, 'candidato.html', dados)

        candidato = Candidato.objects.create_user(

            nome = nome,
            username = cpf,
            data_nascimento = data_nascimento,
            covid= covid,
            password = senha
        )

        candidato.save()

        dicionario = carregar_grupos_atendimento()
        grupos = dicionario['grupos']['grupoatendimento']

        for grupo in grupos:
            nome = grupo['nome']
            _, created = GrupoAtendimento.objects.get_or_create(nome=nome)

        candidato.grupo_atendimento.set(grupo_atendimento)

        resposta = apto(data_nascimento, covid, grupo_atendimento)

        avisos = {"apto": resposta, "cadastro": 'Cadastro realizado com sucesso!' }

        return render(request, 'login.html', avisos)


def login_user(request):

    if request.method == "GET":
        return render(request, 'login.html')
    

    if request.method == "POST":
        cpf = request.POST.get('cpf')
        senha = request.POST.get('senha')

        candidato = authenticate(request, username=cpf, password=senha)

        if candidato is not None:
            login(request, candidato)

            id = request.user.id

            usuario = Candidato.objects.get(id=id)
            
            grupoAtendimento = []

            nome = usuario.nome
            data_nascimeto = usuario.data_nascimento
            idade = calcular_idade(data_nascimeto)
            cpf = request.user.username

            for grupo in usuario.grupo_atendimento.all():
                grupoAtendimento.append(grupo.id)
                
            apitidao = apto(data_nascimeto.strftime("%Y-%m-%d"), str(usuario.covid), grupoAtendimento)

            if "não" in apitidao:
                apitidao = False
            else:
                apitidao = True

            candidato = {
                "nome": nome,
                "data_nascimento": data_nascimeto,
                "idade": idade,
                "cpf": cpf,
                "apto": apitidao
            }
            return render(request, 'candidato_logado.html', candidato)
        else:
            return render(request, 'login.html', {"erro_login": 'CPF ou senha inválidos!'})
        

def logout_user(request):
    logout(request)
    return redirect('login')


@login_required
def pagina_candidato(request):
    if request.method == "GET":
        id = request.user.id

        usuario = Candidato.objects.get(id=id)
        
        grupoAtendimento = []

        nome = usuario.nome
        data_nascimeto = usuario.data_nascimento
        idade = calcular_idade(data_nascimeto)
        cpf = request.user.username

        for grupo in usuario.grupo_atendimento.all():
            grupoAtendimento.append(grupo.id)
            
        apitidao = apto(data_nascimeto.strftime("%Y-%m-%d"), str(usuario.covid), grupoAtendimento)

        if "não" in apitidao:
            apitidao = False
        else:
            apitidao = True

        candidato = {
            "nome": nome,
            "data_nascimento": data_nascimeto,
            "idade": idade,
            "cpf": cpf,
            "apto": apitidao
        }

        return render(request, 'candidato_logado.html', candidato)
          

