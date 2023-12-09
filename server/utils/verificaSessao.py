from server.models import Sessao
from django.utils import timezone


def verificarSessao( token ):
    try:
        sessao = Sessao.objects.get(token=token)
        dataAtual = timezone.now().date()
        
        if sessao.dataExpiracao < dataAtual:
            Sessao.objects.get(id=sessao.id).delete()
            return False

        return True

    except:
        return False