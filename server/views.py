from datetime import timedelta
from django.utils import timezone
from django.shortcuts import HttpResponseRedirect
from .models import Usuario, Sessao
import string
import random

def random_generator(size=15, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def verificarSessão( token ) -> bool:
    sessao = Sessao.objects.get(token=token)
    dataAtual = timezone.now().date()

    if sessao is None or sessao.dataExpiracao < dataAtual:
        return False

    return True

def firstLoginServer( request, id ):
    if request.method != 'POST':
        return '405 Method Not Allowed'

    user = Usuario.objects.get(id=id)

    user.senha = request.POST['senha']
    user.telefone = request.POST['telefone']

    user.save()

    return HttpResponseRedirect("/inicio")

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

