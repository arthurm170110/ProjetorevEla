from django.urls import path
from . import views



urlpatterns = [

    path('', views.cadastro_agendamento, name="agendamentos"),
    path('listagem/', views.lista_agendamento, name="listagem"),
    path('carregar_datas_disponiveis/<int:estabelecimento>/', views.carregar_datas_disponiveis_view, name='carregar_datas_disponiveis'),
    path('obter_hora/', views.obter_hora_view, name='obter_hora'),
    
]