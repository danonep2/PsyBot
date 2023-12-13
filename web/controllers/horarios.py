from server.utils.verificaSessao import verificarSessao
from django.shortcuts import HttpResponseRedirect, render
from django.utils import timezone
from server.models import Cosultas

days_of_week = {
    'Sunday': 1,
    'Monday': 2,
    'Tuesday': 3,
    'Wednesday': 4,
    'Thursday': 5,
    'Friday': 6,
    'Saturday': 7,
}

def horarios( request ):
    isTokenValid = verificarSessao(request)

    if not isTokenValid:
        return HttpResponseRedirect(request, 'login.html')
    
    usuario = isTokenValid

    currentDay = timezone.now().date().strftime('%A')
    dayOfWeek = days_of_week[currentDay]

    print('\n\n\n')
    print('dia da semana: ', dayOfWeek)

    initial = dayOfWeek - 1

    initialDate = timezone.now().date() + timezone.timedelta(days=-initial)
    finalDate = timezone.now().date() + timezone.timedelta(days=7 - initial  - 1)

    print('range: ', initialDate, finalDate)

    consultQuery = Cosultas.objects.filter(data__range=[
        str(initialDate),
        str(finalDate)
    ])

    finalData = [[None, None, None, None], #segunda
                 [None, None, None, None], #terça
                 [None, None, None, None], #quarta
                 [None, None, None, None], #quinta
                 [None, None, None, None]] #sexta

    for consult in consultQuery:
        if 8 <= consult.horario <= 11:
            weekDay = consult.data.strftime('%A')
            weekDay = days_of_week[weekDay]
            finalData[weekDay -2][consult.horario - 8] = consult

    for i in finalData:
        print(i)

    hours = ['08:00', '09:00', '10:00', '11:00']

    table = ''

    createConsultEl = '''
        <td class="livre">
            <a onclick="confirmarCriacao({},{})" href="#">
                    Livre
            </a>
        </td>
    '''

    for i in range(0, 4):
        table += '<tr>'
        table += '<td>' + hours[i] + '</td>'
        for j in range(0, 5):
            if usuario.tipo == 'psicologa' and finalData[j][i] is not None:
                table += f'<td class="ocupado">{finalData[j][i].usuario.nome.split()[0]}</td>'

            elif finalData[j][i] is None and usuario.tipo == 'psicologa':
                table += '<td class="livre"><a href="#">Livre</a></td>'

            elif finalData[j][i] is None:
                table += createConsultEl.format(j + 1, i + 8)

            elif finalData[j][i].usuario == usuario:
                table += '<td class="minha-consulta" style="color: green">Sua consulta</td>'

            else:
                table += '<td class="ocupado">Ocupado</td>'
        table += '</tr>'

    msg = request.session.pop('msg_horario', "")

    data = {
        'table' : table,
        'msg' : msg,
        'user' : usuario.nome.split()[0],
    }

    if usuario.tipo == 'psicologa':
        return render(request, 'horarios_psi.html', data)

    return render(request, 'horarios.html', data)
