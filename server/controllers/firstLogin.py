from django.shortcuts import HttpResponseRedirect
from server.utils.verificaSessao import verificarSessao

from server.models import Usuario

def firstLoginServer( request ):
    if request.method != 'POST':
        return '405 Method Not Allowed'
    
    isTokenValid = verificarSessao(request)

    if not isTokenValid:
        return HttpResponseRedirect('/login')

    user = isTokenValid

    senha = request.POST['senha']
    confirmar_senha = request.POST['confirmar_senha']
    
    if senha != confirmar_senha:
        request.session['error_message'] = '<p style="color: red;"> Senhas não coincidem </p>'
        return HttpResponseRedirect("/primeiro-login")
    
    user.senha = senha

    user.save()

    return HttpResponseRedirect("/dashboard")