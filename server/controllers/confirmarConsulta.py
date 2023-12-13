from django.shortcuts import HttpResponseRedirect
from django.utils import timezone
from server.models import Cosultas
from server.utils.verificaSessao import verificarSessao

def confirmarConsulta( request ):
    isTokenValid = verificarSessao(request)

    if not isTokenValid:
        return HttpResponseRedirect(request, 'login.html')
    
    usuario = isTokenValid

    if usuario.tipo == 'aluno':
        return HttpResponseRedirect(request, 'dashboard.html')

    idConsulta = int(request.POST['id'])
    remarcar = bool(request.POST['remarcar'])
    presente = bool(request.POST['presente'])
    desc = request.POST['desc']

    consulta = Cosultas.objects.get(id=idConsulta)
    consulta.pendente = False
    consulta.descricao = desc
    consulta.presente = presente

    usuario = consulta.usuario
    numeroConsulta = usuario.numeroConsultas

    if remarcar:
        novaConsulta = Cosultas()
        novaConsulta.usuario = usuario
        novaConsulta.data = consulta.data + timezone.timedelta(days=7)

        if presente:
            novaConsulta.numeroConsulta += numeroConsulta + 1
    
    return HttpResponseRedirect('dashboard')

