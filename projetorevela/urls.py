from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('candidato/', include('candidato.urls')),
    path('', include('candidato.urls'))
]
