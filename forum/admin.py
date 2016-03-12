from django.contrib import admin
from .models import Pregunta, Respuesta, Votos


admin.site.register(Pregunta)
admin.site.register(Respuesta)
admin.site.register(Votos)
