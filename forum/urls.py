from django.conf.urls import url
from .views import ListaPreguntas, DetallePregunta, CrearPregunta, CrearRespuesta

urlpatterns = [
    url(r'^$', ListaPreguntas.as_view(), name="lista_preguntas"),
    url(r'^crear-pregunta/$', CrearPregunta.as_view(), name='crear_pregunta'),
    url(r'^responder/(?P<slug>[-\w]+)/$', CrearRespuesta.as_view(), name='crear_respuesta'),
    url(r'^detalle-pregunta/(?P<slug>[-\w]+)/$', DetallePregunta.as_view(),
        name="detalle_pregunta"),
]
