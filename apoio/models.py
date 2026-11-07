import secrets

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models


def _provas_storage():
    # pasta privada, sem URL pública: o download passa pela view da coordenação
    return FileSystemStorage(location=settings.PROVAS_DIR, base_url=None)

# Sem letras/números ambíguos (0/O, 1/I/L): o aluno vai digitar isso depois.
_ALFABETO = "ABCDEFGHJKMNPQRSTUVWXYZ23456789"


def novo_protocolo() -> str:
    parte = lambda: "".join(secrets.choice(_ALFABETO) for _ in range(4))
    return f"ESC-{parte()}-{parte()}"


class Denuncia(models.Model):
    """Um relato. Guarda o FATO (o que, onde, quando), nunca um perfil emocional do aluno."""

    class Tipo(models.TextChoices):
        OFENSA = "ofensa", "Ofensas ou humilhação"
        EXPOSICAO = "exposicao", "Exposição de foto, vídeo ou conversa"
        AMEACA = "ameaca", "Ameaça"
        DISCRIMINACAO = "discriminacao", "Discriminação (racismo, LGBTfobia, etc.)"
        PERFIL_FALSO = "perfil_falso", "Perfil falso se passando por alguém"
        EXCLUSAO = "exclusao", "Exclusão proposital de grupos"
        OUTRO = "outro", "Outro"

    class Plataforma(models.TextChoices):
        WHATSAPP = "whatsapp", "WhatsApp"
        INSTAGRAM = "instagram", "Instagram"
        TIKTOK = "tiktok", "TikTok"
        DISCORD = "discord", "Discord"
        JOGO = "jogo", "Jogo online"
        OUTRA = "outra", "Outra"

    class Status(models.TextChoices):
        RECEBIDA = "recebida", "Recebida"
        ANALISE = "analise", "Em análise"
        ACOMPANHAMENTO = "acompanhamento", "Em acompanhamento"
        ENCERRADA = "encerrada", "Encerrada"

    class Quem(models.TextChoices):
        COMIGO = "comigo", "Aconteceu comigo"
        COLEGA = "colega", "Vi acontecer com um colega"

    protocolo = models.CharField(max_length=13, unique=True, default=novo_protocolo, editable=False)
    quem = models.CharField(max_length=10, choices=Quem.choices, default=Quem.COMIGO)
    tipo = models.CharField(max_length=20, choices=Tipo.choices)
    plataforma = models.CharField(max_length=20, choices=Plataforma.choices)
    quando = models.CharField("Quando aconteceu", max_length=60, blank=True,
                              help_text="Ex.: ontem à noite, semana passada, ainda está acontecendo")
    descricao = models.TextField("O que aconteceu", max_length=3000)
    prova = models.FileField("Print ou arquivo (opcional)", storage=_provas_storage, upload_to="%Y/%m", blank=True)
    anonima = models.BooleanField(default=True)
    nome = models.CharField(max_length=100, blank=True)
    contato = models.CharField("Turma ou contato", max_length=100, blank=True)
    risco = models.BooleanField("Alguém corre risco agora", default=False)

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.RECEBIDA)
    resposta = models.TextField("Mensagem para quem relatou", blank=True)
    criada = models.DateTimeField(auto_now_add=True)
    atualizada = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-risco", "-criada"]

    @property
    def urgente(self) -> bool:
        return self.risco or self.tipo == self.Tipo.AMEACA

    def save(self, *args, **kwargs):
        if self.anonima:  # anônimo de verdade: nem guarda o que foi digitado
            self.nome = self.contato = ""
        super().save(*args, **kwargs)
