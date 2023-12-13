from django.shortcuts import render, HttpResponseRedirect
from server.models import Consultas
from django.utils import timezone
from server.utils.verificaSessao import verificarSessao

from web.controllers.horarios import horarios

# Create your views here.
def login( request):
    error = request.session.pop('error_message', "")
    print('error: ', error)

    return render(request, 'login.html', {'error': error})

def primeiroLogin( request ):
    isTokenValid = verificarSessao(request)
    if not isTokenValid:
        return HttpResponseRedirect(request, 'login.html')
    
    error = request.session.pop('error_message', "")
    return render(request, 'redefinir_senha.html', {'error': error})

def formatDate( date ):
    date = date.split('-')
    date.reverse()
    date = '/'.join(date)
    return date

def dashboard( request ):
    isTokenValid = verificarSessao(request)

    if not isTokenValid:
        return HttpResponseRedirect(request, 'login.html')
    
    usuario = isTokenValid

    if usuario.tipo == 'aluno':
        try:
            consulta = Consultas.objects.get(usuario=usuario, pendente=True)
            data = {
                'proxima_consulta':  f'''
            <table class="table table-hover">
                <tr>
                    <td> {consulta.usuario.nome.split()[0]} </td>
                    <td> {formatDate(str(consulta.data))}</td>
                    <td> {consulta.horario}:00 h </td>
                    <td> {consulta.numeroConsulta} ª</td>
                </tr>
            </table>
            ''',
                'user': usuario.nome.split()[0]
            }

        except:
            data ={
                'proxima_consulta':'<p> <center> Sem Consultas </center> </p>',
                'user': usuario.nome.split(' ')[0]
            }

        return render(request, 'dashboard.html', data)
    
    consultas = Consultas.objects.filter(pendente=True).order_by('data', 'horario')

    response = '<center> <h1> Sem consultas Pendentes </h1> </center> <br>'

    if len(consultas) > 0:
        response = ''
        for consulta in consultas:
            response += f'''
            <tr>
                <td> {consulta.usuario.nome.split()[0]} </td>
                <td> {formatDate(str(consulta.data))}</td>
                <td> {consulta.horario}:00 h </td>
                <td> {consulta.numeroConsulta} ª</td>
                <td> <a href="/confirmar/{consulta.id}" class="botao"> Confirmar </a></td>
            </tr>
'''
    data = {
        'rows': response,
        'user': usuario.nome.split(' ')[0],
    }

    return render(request, 'dashPsy.html', data)



def sobre( request ):
    isTokenValid = verificarSessao(request)

    user = isTokenValid

    data = {
        'user': user.nome.split(' ')[0]
    }

    if not isTokenValid:
        return HttpResponseRedirect(request, 'login.html')
    
    return render(request, 'sobre.html', data)

def suporte( request ):
    isTokenValid = verificarSessao(request)
    
    user = isTokenValid

    data = {
        'user': user.nome.split(' ')[0]
    }

    if not isTokenValid:
        return HttpResponseRedirect(request, 'login.html')
    
    return render(request, 'suporte.html', data)

def confirmar( request, id ):
    isTokenValid = verificarSessao(request)

    if not isTokenValid:
        return HttpResponseRedirect(request, 'login.html')

    user = isTokenValid

    try:
        consulta = Consultas.objects.get(id=id)
        data = {
            'nomeAluno': consulta.usuario.nome.split()[0],
            'idConsulta': consulta.id,
            'user': user.nome.split(' ')[0]
        }

        return render(request, 'confirmar.html', data)

    except: pass

    return HttpResponseRedirect(request, 'dashboard.html')