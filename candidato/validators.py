from rest_framework import serializers
from django.core.exceptions import ValidationError

from validate_docbr import CPF


def cpf_valido(cpf):
    if len(cpf) != 11:
        raise ValidationError({'cpf': 'CPF não possui apenas 11 caracteres.'})
    numero_cpf = CPF()
    if not numero_cpf.validate(cpf):
        raise ValidationError({'cpf': 'CPF inválido.'})
    return cpf