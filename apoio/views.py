from pathlib import Path

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render

from .forms import DenunciaForm, RespostaForm
from .models import Denuncia

staff = staff_member_required(login_url="login")


#alunos

def inicio(request):
    return render(request, "apoio/inicio.html")


def guia(request):
    return render(request, "apoio/guia.html")


FRASES_COLEGA = [
    {"texto": "Vi o que mandaram no grupo. Isso foi zoado e não tem nada a ver com você. Tô aqui se quiser conversar."},
    {"texto": "Quer que eu vá com você falar com alguém da escola? Ou prefere que eu avise sem falar seu nome?"},
    {"texto": "Denunciei o post. Se aparecer mais coisa, me fala que eu ajudo a guardar os prints."},
    {"texto": "Gente, isso passou do limite. Bora parar de compartilhar.", "grupo": True},
]


def colega(request):
    return render(request, "apoio/colega.html", {"frases": FRASES_COLEGA})


def denunciar(request):
    form = DenunciaForm(request.POST or None, request.FILES or None,
                        initial={"quem": request.GET.get("quem", "comigo")})
    if form.is_valid():
        d = form.save()
        request.session["ultimo_protocolo"] = d.protocolo
        return redirect("enviada")
    return render(request, "apoio/denunciar.html", {"form": form})


def enviada(request):
    protocolo = request.session.pop("ultimo_protocolo", None)
    if not protocolo:
        return redirect("inicio")
    d = Denuncia.objects.get(protocolo=protocolo)
    return render(request, "apoio/enviada.html", {"d": d})


def acompanhar(request):
    d, erro = None, False
    codigo = request.POST.get("protocolo", "").strip().upper()
    if codigo:
        d = Denuncia.objects.filter(protocolo=codigo).first()
        erro = d is None
    return render(request, "apoio/acompanhar.html", {"d": d, "erro": erro, "codigo": codigo})


#coordenação
@staff
def painel(request):
    qs = Denuncia.objects.all()
    status = request.GET.get("status")
    if status:
        qs = qs.filter(status=status)
    todas = Denuncia.objects.all()
    total = todas.count() or 1

    def contagem(campo, choices):
        nomes = dict(choices)
        linhas = [{"nome": nomes[r[campo]], "n": r["n"], "pct": round(100 * r["n"] / total)}
                  for r in todas.values(campo).annotate(n=Count("id")).order_by("-n")]
        return linhas

    return render(request, "apoio/painel.html", {
        "denuncias": qs,
        "status_atual": status,
        "status_choices": Denuncia.Status.choices,
        "abertas": todas.exclude(status=Denuncia.Status.ENCERRADA).count(),
        "urgentes": sum(1 for d in todas.exclude(status=Denuncia.Status.ENCERRADA) if d.urgente),
        "por_tipo": contagem("tipo", Denuncia.Tipo.choices),
        "por_plataforma": contagem("plataforma", Denuncia.Plataforma.choices),
    })


@staff
def detalhe(request, pk):
    d = get_object_or_404(Denuncia, pk=pk)
    form = RespostaForm(request.POST or None, instance=d)
    if form.is_valid():
        form.save()
        return redirect("detalhe", pk=pk)
    return render(request, "apoio/detalhe.html", {"d": d, "form": form})


@staff
def prova(request, pk):
    d = get_object_or_404(Denuncia, pk=pk)
    if not d.prova:
        raise Http404
    return FileResponse(d.prova.open("rb"), filename=Path(d.prova.name).name)
