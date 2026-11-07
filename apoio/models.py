from django.db import models

from .protocolos import novo_protocolo
from .storage import provas_storage


class Denuncia(models.Model):

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
    prova = models.FileField("Print ou arquivo (opcional)", storage=provas_storage, upload_to="%Y/%m", blank=True)
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

    # Ícones (Bootstrap Icons) usados na lista da coordenação
    ICONES_TIPO = {"ofensa": "bi-chat-left-text", "exposicao": "bi-image", "ameaca": "bi-exclamation-octagon",
                   "discriminacao": "bi-slash-circle", "perfil_falso": "bi-person-bounding-box",
                   "exclusao": "bi-people", "outro": "bi-three-dots"}
    ICONES_PLATAFORMA = {"whatsapp": "bi-whatsapp", "instagram": "bi-instagram", "tiktok": "bi-tiktok",
                         "discord": "bi-discord", "jogo": "bi-controller", "outra": "bi-globe"}

    @property
    def icone_tipo(self) -> str:
        return self.ICONES_TIPO.get(self.tipo, "bi-three-dots")

    @property
    def icone_plataforma(self) -> str:
        return self.ICONES_PLATAFORMA.get(self.plataforma, "bi-globe")

    @property
    def etapa(self) -> int:
        """Posição do status (1..4), para a linha do tempo."""
        return list(self.Status.values).index(self.status) + 1

    @property
    def urgente(self) -> bool:
        return self.risco or self.tipo == self.Tipo.AMEACA

    def save(self, *args, **kwargs):
        if self.anonima: 
            self.nome = self.contato = ""
        super().save(*args, **kwargs)
