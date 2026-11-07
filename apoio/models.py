from django.db import models

from .protocolos import novo_protocolo
from .storage import provas_storage


class Denuncia(models.Model):
    TIPO_CHOICES = [
        ("ofensa", "Ofensas ou humilhação"),
        ("exposicao", "Exposição de foto, vídeo ou conversa"),
        ("ameaca", "Ameaça"),
        ("discriminacao", "Discriminação (racismo, LGBTfobia, etc.)"),
        ("perfil_falso", "Perfil falso se passando por alguém"),
        ("exclusao", "Exclusão proposital de grupos"),
        ("outro", "Outro"),
    ]
    PLATAFORMA_CHOICES = [
        ("whatsapp", "WhatsApp"),
        ("instagram", "Instagram"),
        ("tiktok", "TikTok"),
        ("discord", "Discord"),
        ("jogo", "Jogo online"),
        ("outra", "Outra"),
    ]
    STATUS_CHOICES = [
        ("recebida", "Recebida"),
        ("analise", "Em análise"),
        ("acompanhamento", "Em acompanhamento"),
        ("encerrada", "Encerrada"),
    ]
    QUEM_CHOICES = [
        ("comigo", "Aconteceu comigo"),
        ("colega", "Vi acontecer com um colega"),
    ]

    protocolo = models.CharField(max_length=13, unique=True, default=novo_protocolo, editable=False)
    quem = models.CharField(max_length=10, choices=QUEM_CHOICES, default="comigo")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    plataforma = models.CharField(max_length=20, choices=PLATAFORMA_CHOICES)
    quando = models.CharField("Quando aconteceu", max_length=60, blank=True,
                              help_text="Ex.: ontem à noite, semana passada, ainda está acontecendo")
    descricao = models.TextField("O que aconteceu", max_length=3000)
    prova = models.FileField("Print ou arquivo (opcional)", storage=provas_storage, upload_to="%Y/%m", blank=True)
    anonima = models.BooleanField(default=True)
    nome = models.CharField(max_length=100, blank=True)
    contato = models.CharField("Turma ou contato", max_length=100, blank=True)
    risco = models.BooleanField("Alguém corre risco agora", default=False)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="recebida")
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
        return [valor for valor, _ in self.STATUS_CHOICES].index(self.status) + 1

    @property
    def urgente(self) -> bool:
        return self.risco or self.tipo == "ameaca"

    def save(self, *args, **kwargs):
        if self.anonima: 
            self.nome = self.contato = ""
        super().save(*args, **kwargs)
