
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
    token = request.COOKIES.get('token')
    isTokenValid = verificarSessao(token)

    if not isTokenValid:
        return HttpResponseRedirect(request, 'login.html')

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
            <a href="/criar-consulta?dayOfWeek={}&hour={}">
                    Livre
            </a>
        </td>
    '''

    for i in range(0, 4):
        table += '<tr>'
        table += '<td>' + hours[i] + '</td>'
        for j in range(0, 5):
            if finalData[j][i] is None:
                table += createConsultEl.format(j + 1, i + 8)
            else:
                table += '<td class="ocupado">Ocupado</td>'
        table += '</tr>'

    data = {
        'table' : table
    }

    return render(request, 'horarios.html', data)
