from django.shortcuts import HttpResponseRedirect, HttpResponse
from django.utils import timezone
from server.utils.verificaSessao import verificarSessao
from server.models import Sessao

def initialRoute(request):
    tokenCookie = request.COOKIES.get('token', 'null')

    isTokenValid = verificarSessao(tokenCookie)

    if not isTokenValid:
        return HttpResponseRedirect('/login')
    
    return HttpResponseRedirect('/dashboard')
    

