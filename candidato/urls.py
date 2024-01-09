from django.urls import path
from . import views


urlpatterns = [
    path('cadastrar/', views.candidatos, name="candidatos"),
    path('', views.paginainicial, name="paginainicial"),
]