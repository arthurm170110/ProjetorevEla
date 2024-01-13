from django.urls import path
from . import views



urlpatterns = [

    path('', views.cadastro_agendamento, name="agendamentos"),
    path('listagem/', views.lista_agendamento, name="listagem"),
    
]