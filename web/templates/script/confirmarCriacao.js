const weekDays = ['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado'];

function confirmarCriacao(dayOfWeek, hour) {
    const confimacao = confirm(`Deseja agendar uma consulta para ${weekDays[dayOfWeek]} às ${hour}:00 horas?`);

    if (confimacao) {
        window.location.href = `/criar-consulta?dayOfWeek=${dayOfWeek}&hour=${hour}`;
    }
}