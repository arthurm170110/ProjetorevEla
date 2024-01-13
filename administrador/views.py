from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import permission_required
from candidato.models import Candidato
from agendamento.models import Estabelecimento
from agendamento.utils import carregar_estabelecimentos


def login_admin(request):

    if request.method == "GET":
        return render(request, "login_admin.html")
    
    if request.method == "POST":
        cpf = request.POST.get('cpf')
        senha = request.POST.get('senha')

        candidato = authenticate(request, username=cpf, password=senha)

        if candidato is not None:
            admin = Candidato.objects.get(id=candidato.id)
            if admin.is_superuser:
                login(request, candidato)
                estabelecimentos = carregar_estabelecimentos()
                lista_estabelecimento = estabelecimentos['estabelecimentos']['estabelecimento']
                return render(request, 'estabelecimentos.html', {"mensagem_sucesso": "Login Realizado com sucesso!", "estabelecimentos": lista_estabelecimento, "lista_estabeleciemento": True})
            else:
                return render(request, 'login_admin.html', {"mensagem_erro": "Você não tem permissão!"})
            
        else:
            return render(request, 'login_admin.html', {"mensagem_erro": "Usuário ou senha inválidos!"})


@permission_required('is_superuser')
def lista_estabelecimentos(request):
    if request.method == "GET":
        busca = request.GET.get('busca', '')
        estabelecimentos = carregar_estabelecimentos()
        lista_estabelecimento = estabelecimentos['estabelecimentos']['estabelecimento']
        if busca:
            lista_estabelecimento = [e for e in lista_estabelecimento if busca.lower() in e['no_fantasia'].lower()]
        if not lista_estabelecimento:
            lista_estabelecimento = estabelecimentos['estabelecimentos']['estabelecimento']
            lista_estabelecimento = [e for e in lista_estabelecimento if busca.lower() in e['co_cnes'].lower()]
        if not lista_estabelecimento:   
            return render(request, 'estabelecimentos.html', {"mensagem_erro": "Nenhum estabelecimento encontrado com o nome ou código fornecido.", "lista_estabeleciemento": True})

        return render(request, 'estabelecimentos.html', {"estabelecimentos": lista_estabelecimento, "lista_estabeleciemento": True})


def logout_admin(request):
    logout(request)
    return redirect('login_admin')