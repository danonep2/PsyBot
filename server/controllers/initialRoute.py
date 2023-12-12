from django.shortcuts import HttpResponseRedirect, HttpResponse
from server.utils.verificaSessao import verificarSessao
from server.models import Sessao

def initialRoute(request):
    tokenCookie = request.COOKIES.get('token', 'null')

    isTokenValid = verificarSessao(tokenCookie)

    if not isTokenValid:
        response  = HttpResponseRedirect('/login')
        response.delete_cookie('token')
        return response
    
    # Coletando senha do usuário do formalario
    senha = request.POST['senha']

    #alterando a senha do usuário
    sessao = Sessao.objects.get(token=tokenCookie)
    sessao.usuario.senha = senha
    sessao.usuario.save()

    return HttpResponseRedirect('/dashboard')
