from django.conf.urls import url
from .views import ListaPreguntas, DetallePregunta, CrearPregunta, CrearRespuesta

urlpatterns = [
    url(r'^$', ListaPreguntas.as_view(), name="lista_preguntas"),
    url(r'^crear_pregunta/$', CrearPregunta.as_view(), name='crear_pregunta'),
    url(r'^crear_respuesta/$', CrearRespuesta.as_view(), name='crear_respuesta'),
    url(r'^(?P<slug>[-\w]+)/$', DetallePregunta.as_view(),
        name="detalle_pregunta"),
]
