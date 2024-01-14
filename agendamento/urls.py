from django.urls import path
from . import views



urlpatterns = [

    path('', views.cadastro_agendamento, name="agendamentos"),
    path('listagem/', views.lista_agendamento, name="listagem"),
    path('obter-datas-disponiveis/<int:estabelecimento>/', views.obter_datas_disponiveis_view, name='obter-datas-disponiveis'),
    path('obter_hora/', views.obter_hora_view, name='obter_hora'),
    
]