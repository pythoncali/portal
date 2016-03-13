from django.contrib import admin
from .models import Pregunta, Respuesta, Votos


@admin.register(Votos)
class VotosAdmin(admin.ModelAdmin):
    fields = ('voto',)
    list_display = ['__str__', 'voto']


@admin.register(Pregunta)
class PreguntaAdmin(admin.ModelAdmin):
    fields = ('titulo', 'descripcion', 'tags')
    list_display = ['titulo', 'tiene_respuesta', 'total_votos', 'etiquetas']

    def etiquetas(self, obj):
        return obj.tags.all()

    def total_votos(self, obj):
        return obj.votos.count()

    def save_model(self, request, obj, form, change):
        obj.autor = request.user
        obj.save()


@admin.register(Respuesta)
class RespuestaAdmin(admin.ModelAdmin):
    fields = ('pregunta', 'descripcion', 'tags')
    list_display = ['descripcion', 'aceptada', 'votacion',
                    'total_votos', 'etiquetas']

    def etiquetas(self, obj):
        return obj.tags.all()

    def total_votos(self, obj):
        return obj.votos.count()

    def votacion(self, obj):
        up_votos = obj.votos.filter(voto=1).count()
        down_votos = obj.votos.filter(voto=-1).count()
        votacion = up_votos - down_votos
        return votacion

    def save_model(self, request, obj, form, change):
        obj.autor = request.user
        obj.save()
