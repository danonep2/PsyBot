from django.shortcuts import HttpResponseRedirect
from server.models import Sessao

def logoutServer(request):
    response = HttpResponseRedirect('/')
    response.delete_cookie('token')

    Sessao.objects.get(token=request.COOKIES.get('token')).delete()

    return response