from django.urls import path
from .views import CandidatoListCreateView, GrupoAtendimentoListView


urlpatterns = [
    path('candidato/', CandidatoListCreateView.as_view(), name='lista-cria-candidato'),
    path('grupo-atendimento/', GrupoAtendimentoListView.as_view(), name='lista-grupo-atendimento'),
]