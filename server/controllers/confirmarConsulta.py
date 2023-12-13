from django.shortcuts import HttpResponseRedirect
from django.utils import timezone
from server.models import Consultas
from server.utils.verificaSessao import verificarSessao

def confirmarConsulta( request ):
    isTokenValid = verificarSessao(request)

    if not isTokenValid:
        return HttpResponseRedirect(request, 'login.html')
    
    usuario = isTokenValid

    if usuario.tipo == 'aluno':
        return HttpResponseRedirect(request, 'dashboard.html')

    idConsulta = int(request.POST['id'])
    remarcar = request.POST['remarcar']
    presente = request.POST['presente']
    desc = request.POST['desc']

    consulta = Consultas.objects.get(id=idConsulta)
    consulta.pendente = False
    consulta.descricao = desc
    consulta.estevePresente = bool(presente)
    consulta.save()

    usuario = consulta.usuario
    numeroConsulta = consulta.numeroConsulta

    if remarcar == "True" and consulta.numeroConsulta <= 10:
        novaConsulta = Consultas()
        novaConsulta.usuario = usuario
        novaConsulta.data = consulta.data + timezone.timedelta(days=7)
        novaConsulta.horario = consulta.horario
        novaConsulta.pendente = True
        novaConsulta.numeroConsulta = numeroConsulta 

        if presente:
            novaConsulta.numeroConsulta += 1
    
        novaConsulta.save()

    return HttpResponseRedirect('/dashboard')

