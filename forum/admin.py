from django.contrib import admin
from .models import Pregunta, Respuesta, Votos


@admin.register(Votos)
class VotosAdmin(admin.ModelAdmin):
    fields = ('voto',)
    list_display = ['__str__', 'voto']

    def save_model(self, request, obj, form, change):
        obj.votante = request.user
        obj.save()


@admin.register(Pregunta)
class PreguntaAdmin(admin.ModelAdmin):
    fields = ('titulo', 'descripcion', 'tags')
    list_display = ['titulo', 'tiene_respuesta']

    def save_model(self, request, obj, form, change):
        obj.autor = request.user
        obj.save()


@admin.register(Respuesta)
class RespuestaAdmin(admin.ModelAdmin):
    fields = ('pregunta', 'descripcion', 'tags')
    list_display = ['descripcion', 'aceptada']

    def save_model(self, request, obj, form, change):
        obj.autor = request.user
        obj.save()
