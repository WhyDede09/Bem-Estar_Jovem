from django.contrib import admin
from apoio.models import Denuncia
# Register your models here.

class DenunciaAdmin (admin.ModelAdmin):
    pass






admin.site.register(Denuncia, DenunciaAdmin)