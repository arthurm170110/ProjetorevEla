from django.utils import timezone
from datetime import datetime
import re

from validate_docbr import CPF
from .models import Candidato


def cpf_valido(cpf):
    if len(cpf) != 11:
        return 'CPF não possui apenas 11 caracteres.'
    numero_cpf = CPF()
    if not numero_cpf.validate(cpf):
        return 'CPF inválido.'
    if Candidato.objects.filter(cpf=cpf).exists():
        return 'Este CPF já foi cadastrado.'

def data_nascimento_valida(data_nascimento):
    data_nascimento_str = data_nascimento
    data_nascimento = datetime.strptime(data_nascimento_str, "%Y-%m-%d").date() 
    if data_nascimento > timezone.now().date():
        return 'Data de nascimento esta a frente da data atual.'
    diferenca_anos = (timezone.now().date() - data_nascimento).days // 365
    if diferenca_anos >= 120:
        return 'A idade não está dentro do intervalo permitido, de até 120 anos.'

def senha_valida(senha):
    erros = []

    if len(senha) < 8:
        erros.append('A senha deve possuir no mínimo 8 caracteres.')
    
    if not re.search(r'[0-9]', senha):
        erros.append('A senha deve possuir pelo menos um número.')

    if not re.search(r'[A-Z]', senha):
        erros.append('A senha deve possuir pelo menos uma letra maiúscula.')

    if not re.search(r'[a-z]', senha):
        erros.append('A senha deve possuir pelo menos uma letra minúscula.')

    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', senha):
        erros.append('A senha deve possuir pelo menos uma caracter especial.')

    return erros
    
def confirma_senha_valida(senha, confirma_senha):
    if senha != confirma_senha:
        return 'A senha deve ser igual.'

def cadastro_valido(cpf, data_nascimento, senha, confirma_senha):
    mensagens_erro = []

    if cpf_valido(cpf):
        mensagens_erro.append({'CPF': cpf_valido(cpf)})

    if data_nascimento_valida(data_nascimento):
        mensagens_erro.append({'data_nascimento': data_nascimento_valida(data_nascimento)})

    if senha_valida(senha):
        mensagens_erro.append({'senha': senha_valida(senha)})

    if confirma_senha_valida(senha, confirma_senha):
        mensagens_erro.append({'confirma_senha': confirma_senha_valida(senha, confirma_senha)})

    
    
    return mensagens_erro
    
   
