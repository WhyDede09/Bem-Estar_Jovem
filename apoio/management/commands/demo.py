"""python manage.py demo — coordenação + relatos FICTÍCIOS para apresentar (apaga os relatos atuais)."""
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from apoio.models import Denuncia

SENHA = "coord1234"

# (quem, tipo, plataforma, quando, descricao, risco, anonima, nome, contato, status, resposta, horas atrás)
RELATOS = [
    ("comigo", "exposicao", "whatsapp", "ontem à noite",
     "Mandaram uma foto minha de quando eu caí na educação física no grupo da sala com figurinhas zoando. "
     "Já tem gente de outras turmas compartilhando. Não quero ir pra escola amanhã.",
     False, True, "", "", "analise", "Recebemos. Já estamos falando com os responsáveis pelo grupo para a foto ser apagada. "
     "Se quiser conversar, a orientadora Paula fica na sala 12 durante o intervalo, é só aparecer.", 20),
    ("colega", "ameaca", "instagram", "hoje",
     "Um perfil falso está mandando mensagem para uma menina do 2ºB dizendo que vai esperar ela na saída.",
     True, True, "", "", "recebida", "", 1),
    ("comigo", "discriminacao", "discord", "semana passada",
     "No servidor da turma ficam fazendo piada com meu cabelo e meu sotaque toda vez que eu entro na call.",
     False, False, "Lucas F.", "1º A", "acompanhamento",
     "Lucas, conversamos com a turma sobre respeito e os moderadores do servidor foram orientados. "
     "Vamos te chamar na quinta para saber como você está.", 96),
    ("colega", "exclusao", "whatsapp", "há umas duas semanas",
     "Criaram um grupo da sala sem uma colega e ficam falando dela lá. Ela percebeu e parou de sentar com a gente.",
     False, True, "", "", "recebida", "", 30),
    ("comigo", "ofensa", "tiktok", "ainda está acontecendo",
     "Fizeram um vídeo imitando meu jeito de falar na apresentação e tá cheio de comentário me xingando.",
     False, True, "", "", "analise", "", 50),
    ("comigo", "perfil_falso", "instagram", "3 dias atrás",
     "Criaram um perfil com meu nome e minhas fotos e estão mandando mensagem estranha para os meus amigos.",
     False, False, "Bianca M.", "3º C", "encerrada",
     "O perfil foi derrubado após denúncia em conjunto com sua família. Qualquer novo perfil, nos avise.", 200),
    ("colega", "ofensa", "jogo", "ontem",
     "No jogo online um grupo da escola fica xingando um garoto do 9º ano no chat de voz toda partida.",
     False, True, "", "", "recebida", "", 8),
]


class Command(BaseCommand):
    help = "Cria usuário da coordenação e relatos fictícios."

    def handle(self, *a, **kw):
        User = get_user_model()
        u, _ = User.objects.get_or_create(username="coordenacao", defaults={"first_name": "Coordenação"})
        u.is_staff = u.is_superuser = True
        u.set_password(SENHA)
        u.save()

        Denuncia.objects.all().delete()
        agora = timezone.now()
        for quem, tipo, plat, quando, desc, risco, anon, nome, contato, status, resp, horas in RELATOS:
            d = Denuncia.objects.create(quem=quem, tipo=tipo, plataforma=plat, quando=quando, descricao=desc,
                                        risco=risco, anonima=anon, nome=nome, contato=contato,
                                        status=status, resposta=resp)
            Denuncia.objects.filter(pk=d.pk).update(criada=agora - timedelta(hours=horas))

        exemplo = Denuncia.objects.filter(resposta__gt="", anonima=True).first()
        self.stdout.write(self.style.SUCCESS(
            f"Coordenação: coordenacao / {SENHA}  |  Protocolo de exemplo (aluno): {exemplo.protocolo}"))
