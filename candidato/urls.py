from django.urls import path
from . import views


urlpatterns = [
    path('cadastrar/', views.candidatos, name="candidatos"),
    path('', views.paginainicial, name="paginainicial"),
    path('login/', views.login_user, name='login'),
    path('candidato/', views.pagina_candidato, name='perfil')
]