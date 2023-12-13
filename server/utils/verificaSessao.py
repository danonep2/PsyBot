from server.models import Sessao
from django.utils import timezone


def verificarSessao( request ):
    try:
        token = request.COOKIES.get('token')
        if token is None:
            return False
        
        sessao = Sessao.objects.get(token=token)
        dataAtual = timezone.now().date()
        
        if sessao.dataExpiracao < dataAtual:
            Sessao.objects.get(id=sessao.id).delete()
            return False

        return sessao.usuario

    except:
        return False