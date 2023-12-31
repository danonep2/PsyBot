"""
URL configuration for PsyBot project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from server.views import *
from web.views import login, dashboard, horarios, sobre, suporte, confirmar, primeiroLogin
from django.urls import path

urlsServer = [
    path('', initialRoute, name='initialRoute'),
    path('admin/', admin.site.urls),
    path('first-loginServer/', firstLoginServer, name='firstLoginServer'),
    path('auth/', auth, name='auth'),
    path('logout/', logoutServer, name='logout'),
    path('criar-consulta/', criarConsulta, name='criarConsulta'),
    path('confirmarConsulta/', confirmarConsulta, name='confirmarConsulta')
]
urlsWeb = [
    path('login/', login, name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('horarios/', horarios, name='horarios'),
    path('sobre/', sobre, name='sobre'),
    path('suporte/', suporte, name='suporte'),
    path('confirmar/<int:id>', confirmar, name='confirmar'),
    path('primeiro-login/', primeiroLogin, name='primeiroLogin')
]

urlpatterns = urlsServer + urlsWeb
