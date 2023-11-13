from django.shortcuts import HttpResponseRedirect

from server.models import Usuario

def firstLoginServer( request, id ):
    if request.method != 'POST':
        return '405 Method Not Allowed'

    user = Usuario.objects.get(id=id)

    user.senha = request.POST['senha']
    user.telefone = request.POST['telefone']

    user.save()

    return HttpResponseRedirect("/inicio")