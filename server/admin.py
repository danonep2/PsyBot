from django.contrib import admin
from .models import Usuario, Sessao, Cosultas

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Sessao)
admin.site.register(Cosultas)