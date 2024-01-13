from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', include('administrador.urls')),
    path('', include('candidato.urls')),
    path('agendamento/', include('agendamento.urls')),
]
