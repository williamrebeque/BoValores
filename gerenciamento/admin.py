from django.contrib import admin
from .models import Ativo, AtivoHistorico

# Register your models here.
admin.site.register(Ativo)
admin.site.register(AtivoHistorico)