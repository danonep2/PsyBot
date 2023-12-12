from django.shortcuts import render, HttpResponseRedirect
from server.models import Cosultas
from django.utils import timezone
from server.utils.verificaSessao import verificarSessao

from web.controllers.horarios import horarios

# Create your views here.
def login( request):
    error = request.session.pop('error_message', "")
    print('error: ', error)

    return render(request, 'login.html', {'error': error})

def dashboard( request ):
    cookie = request.COOKIES.get('token', None)
    isTokenValid = verificarSessao(cookie)

    if not isTokenValid:
        return HttpResponseRedirect(request, 'login.html')
    
    usuario = isTokenValid

    try:
        consulta = Cosultas.objects.get(usuario=usuario, pendente=True)
        data = {
            'proxima_consulta':  f'<p> <center> Proxima consulta: {consulta.data} as {consulta.horario}h </center> </p>'
        }

    except:
        data ={
            'proxima_consulta':'<p> <center> Sem Consultas </center> </p>'
        }

    return render(request, 'dashboard.html', data)
