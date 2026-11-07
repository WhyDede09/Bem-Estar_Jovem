"""Login e logout da coordenação — só funções, sem class-based views nem forms em classe."""
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST


def _destino_seguro(request, destino):
    """Só aceita redirecionar para o próprio site (evita open redirect via ?next=)."""
    return destino and url_has_allowed_host_and_scheme(
        destino, allowed_hosts={request.get_host()}, require_https=request.is_secure()
    )


def entrar(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect("painel")

    destino = request.POST.get("next") or request.GET.get("next", "")
    usuario = request.POST.get("username", "").strip()
    erro = False

    if request.method == "POST":
        user = authenticate(request, username=usuario, password=request.POST.get("password", ""))
        # Só a coordenação (is_staff) entra; mensagem genérica para não revelar se o usuário existe.
        if user is not None and user.is_staff:
            login(request, user)
            return redirect(destino if _destino_seguro(request, destino) else "painel")
        erro = True

    return render(request, "accounts/login.html", {"erro": erro, "next": destino, "usuario": usuario})


@require_POST  # logout por GET deixaria qualquer link/imagem deslogar a coordenação
def sair(request):
    logout(request)
    return redirect("login")
