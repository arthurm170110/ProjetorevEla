from django.shortcuts import render
from django.http import HttpResponse

from .utils import carregar_grupos_atendimento, apto
from .validators import cadastro_valido

from .models import Candidato, GrupoAtendimento

def paginainicial(request):
    return render(request, 'paginainicial.html')

# def cadastrar(request):
#     return render(request, 'cadastro.html')

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
            return render(request, 'candidato.html')

        candidato = Candidato(

            nome = nome,
            cpf = cpf,
            data_nascimento = data_nascimento,
            covid= covid,
            senha = senha
        )

        candidato.save()

        dicionario = carregar_grupos_atendimento()
        grupos = dicionario['grupos']['grupoatendimento']

        for grupo in grupos:
            nome = grupo['nome']
            _, created = GrupoAtendimento.objects.get_or_create(nome=nome)

        candidato.grupo_atendimento.set(grupo_atendimento)

        return HttpResponse('teste')
    

