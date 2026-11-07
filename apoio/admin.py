from django.contrib import admin
from apoio.models import Denuncia
from django.utils import timezone
from django.utils.html import format_html
# Register your models here.

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
    
    @admin.display(description="Prioridade", ordering="risco")
    def alerta(self, obj):
        if obj.risco:
            return format_html('<b style="color:{}">{}</b>', "#c62828", "⚠ RISCO AGORA")
        if obj.urgente:  # ameaça sem risco declarado
            return format_html('<b style="color:{}">{}</b>', "#ef6c00", "▲ Urgente")
        return "—"

    @admin.display(description="Prova anexada")
    def prova_arquivo(self, obj):
        # Não usamos .url: o storage é privado e pode nem ter URL pública.
        return obj.prova.name.rsplit("/", 1)[-1] if obj.prova else "Nenhuma"





admin.site.register(Denuncia, DenunciaAdmin)