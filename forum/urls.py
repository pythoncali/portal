from django.conf.urls import url
from .views import ListaPreguntas, DetallePregunta, CrearPregunta, CrearRespuesta, ComentarPregunta, ComentarRespuesta

urlpatterns = [
    url(r'^$', ListaPreguntas.as_view(), name="lista_preguntas"),
    url(r'^crear-pregunta/$', CrearPregunta.as_view(), name='crear_pregunta'),
    url(r'^responder/(?P<pregunta_id>\d+)/$',
        CrearRespuesta.as_view(), name='crear_respuesta'),
    url(r'^comentar/pregunta/(?P<pregunta_id>\d+)/$',
        ComentarPregunta.as_view(), name='comentar_pregunta'),
    url(r'^comentar/respuesta/(?P<respuesta_id>\d+)/$',
        ComentarRespuesta.as_view(), name='comentar_respuesta'),
    url(r'^detalle-pregunta/(?P<slug>[-\w]+)/$', DetallePregunta.as_view(),
        name="detalle_pregunta"),
]
