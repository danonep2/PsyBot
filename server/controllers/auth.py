import string
import random
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import HttpResponseRedirect, redirect

from server.models import Usuario, Sessao

def random_generator(size=15, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def auth( request ):
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

        if senha == 'Aluno@ifpi':
            response = HttpResponseRedirect('/primeiro-login')
            response.set_cookie('token', novoToken)
            return response

        response.set_cookie('token', novoToken)
        response = HttpResponseRedirect('/')
        return response

    except:
        error = "<p style='color: red'>Usuário ou senha incorretos</p>"
        request.session['error_message'] = error
        return redirect('login')

