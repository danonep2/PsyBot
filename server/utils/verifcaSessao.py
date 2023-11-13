from server.models import Sessao
from django.utils import timezone


def verificarSessao( token ) -> bool:
    sessao = Sessao.objects.get(token=token)
    dataAtual = timezone.now().date()

    if sessao is None:
        return False
    
    if sessao.dataExpiracao < dataAtual:
        Sessao.objects.delete(id=sessao.id)
        return False

    return True