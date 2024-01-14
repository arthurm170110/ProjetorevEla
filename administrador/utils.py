import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
import base64

from agendamento.models import Estabelecimento, Agendamento
from candidato.models import Candidato
from candidato.utils import carregar_informacoes

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph


def carregar_grafico_barra():
    estabelecimentos = Estabelecimento.objects.all()
    agendamentos_por_estabelecimento = [Agendamento.objects.filter(estabelecimento=e).count() for e in estabelecimentos]
    estabelecimentos = [e.nome for e in estabelecimentos]
    plt.bar(estabelecimentos, agendamentos_por_estabelecimento)
    plt.xticks(rotation=90)
    plt.tight_layout()
    return get_graph() 


def carregar_grafico_pizza():
    aptos = 0;
    inaptos = 0;
    candidatos = Candidato.objects.all()
    for candidato in candidatos:
        dados = carregar_informacoes(candidato)
        if dados['apto']:
            aptos = aptos + 1
        else:
            inaptos = inaptos + 1
    plt.pie([aptos, inaptos], labels=['Aptos: ' + str(aptos), 'Inaptos: ' + str(inaptos)], autopct='%1.1f%%')
    return get_graph()