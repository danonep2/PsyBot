from django.shortcuts import HttpResponseRedirect, render
from server.utils.verificaSessao import verificarSessao

def dashboardServer( request ):
    tokenCookie = request.COOKIES.get('token', 'null')

    isTokenValid = verificarSessao(tokenCookie)

    if not isTokenValid:
        return HttpResponseRedirect('/login')

    return render(request, 'dashboard.html')