import string
import random
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import HttpResponseRedirect

from server.models import Usuario, Sessao

def random_generator(size=15, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def loginServer( request ):
    if request.method != 'POST':
        return '405 Method Not Allowed'

    matricula = request.POST['matricula']
    senha = request.POST['senha']

    try:
        user = Usuario.objects.get(matricula=matricula, senha=senha)

        sessao = Sessao()

        novoToken = random_generator()

        dataCriacao = timezone.now().date()
        dataExpiracao = dataCriacao + timedelta(days=2)

        sessao.token = novoToken
        sessao.dataCriacao = dataCriacao
        sessao.dataExpiracao = dataExpiracao
        sessao.usuario = user

        sessao.save()

        return HttpResponseRedirect('/login')

    except:
        return HttpResponseRedirect('/login')

