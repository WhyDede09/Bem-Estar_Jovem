from django.contrib import admin
from apoio.models import Denuncia
from django.utils import timezone
from django.utils.html import format_html


class DenunciaAdmin (admin.ModelAdmin):
    list_display = (
        "protocolo", "alerta", "tipo", "plataforma", "status", "criada"
    )
    list_display_links = ("protocolo",)
    list_filter = ("status", "risco", "tipo", "plataforma", "anonima", "criada",)
    search_fields = ("protocolo", "descricao",)
    date_hierarchy = "criada"
    list_per_page = 30
    show_full_result_count = False

    #Formulário
    readonly_fields = (
        "protocolo", "alerta", "criada", "atualizada",
        "quem", "tipo", "plataforma", "quando", "descricao",
        "prova_arquivo", "anonima", "nome", "contato", "risco",
    )

    def get_fieldsets(self, request, obj=None):
        identidade = ("anonima",) if (obj is None or obj.anonima) else ("anonima", "nome", "contato")
        return (
            ("Identificação", {"fields": ("protocolo", "alerta", "criada", "atualizada")}),
            ("Relato", {"fields": ("quem", "tipo", "plataforma", "quando", "descricao", "prova_arquivo")}),
            ("Quem relatou", {"fields": identidade}),
            ("Atendimento", {
                "fields": ("status", "resposta"),
                "description": "A mensagem abaixo é a que a pessoa verá ao consultar o protocolo.",
            }),
        )

    #Colunas
    @admin.display(description="Prioridade", ordering="risco")
    def alerta(self, obj):
        if obj.risco:
            return format_html('<b style="color:#c62828">⚠ RISCO AGORA</b>')
        if obj.urgente: 
            return format_html('<b style="color:#ef6c00">▲ Urgente</b>')
        return "—"

    @admin.display(description="Prova anexada")
    def prova_arquivo(self, obj):
        return obj.prova.name.rsplit("/", 1)[-1] if obj.prova else "Nenhuma"

    actions = ["marcar_analise", "marcar_acompanhamento", "encerrar"]

    def _mudar_status(self, request, queryset, novo_status):
        n = queryset.update(status=novo_status, atualizada=timezone.now())
        self.message_user(request, f"{n} denúncia(s) atualizada(s).")

    @admin.action(description="Marcar como Em análise")
    def marcar_analise(self, request, queryset):
        self._mudar_status(request, queryset, Denuncia.Status.ANALISE)

    @admin.action(description="Marcar como Em acompanhamento")
    def marcar_acompanhamento(self, request, queryset):
        self._mudar_status(request, queryset, Denuncia.Status.ACOMPANHAMENTO)

    @admin.action(description="Encerrar denúncias")
    def encerrar(self, request, queryset):
        self._mudar_status(request, queryset, Denuncia.Status.ENCERRADA)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser




admin.site.register(Denuncia, DenunciaAdmin)