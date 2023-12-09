from django.shortcuts import render, HttpResponseRedirect
from server.utils.verificaSessao import verificarSessao

# Create your views here.
def login( request ):
    return render(request, 'login.html')

def dashboard( request ):
    cookie = request.COOKIES.get('token', 'null')
    isTokenValid = verificarSessao(cookie)

    if not isTokenValid:
        return HttpResponseRedirect(request, 'login.html')

    return render(request, 'dashboard.html')