from django.http import HttpResponseRedirect
from django.utils import timezone
from web.controllers.horarios import days_of_week
from server.models import Cosultas
from server.utils.verificaSessao import verificarSessao

def criarConsulta(request):
    isTokenValid = verificarSessao(request)

    if not isTokenValid:
        return HttpResponseRedirect(request, 'login.html')
    
    usuario = isTokenValid

    if usuario.tipo == 'psicologa':
        request.session['msg_horario'] = '<center><p style="color: red">Você não pode marcar consulta!</p></center>'
        return HttpResponseRedirect('/horarios')

    # Verificar se o usuario ja tem consulta
    consultas = Cosultas.objects.filter(usuario=usuario)
    if consultas:
        request.session['msg_horario'] = '<center><p style="color: red">Você já tem uma consulta marcada!</p></center>'
        return HttpResponseRedirect('/horarios')
    
    dayOfWeekReq = int(request.GET['dayOfWeek'])
    hour = int(request.GET['hour'])

    currentDay = timezone.now().date().strftime('%A')
    dayOfWeek = days_of_week[currentDay]

    print('\n\n\n')
    print('dia da semana: ', dayOfWeek)

    initial = dayOfWeek - 1
    initialDate = timezone.now().date() + timezone.timedelta(days=-initial)

    consulta = Cosultas()
    consulta.usuario = usuario
    consulta.horario = hour
    consulta.numeroConsulta = 1
    consulta.data = initialDate + timezone.timedelta(days=+dayOfWeekReq)

    consulta.save()

    request.session['msg_horario'] = '<center><p style="color: green">Consulta marcada com sucesso!</p></center>'
    

    return HttpResponseRedirect('/horarios')