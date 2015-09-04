from django.conf.urls import url
from .views import (ListaArticulos, DetalleArticulo, CrearArticulo,
                    CrearCategoria)

# Crear URL's para vistas CrearArticulo y EditarArticulo

urlpatterns = [
    url(r'^$', ListaArticulos.as_view(), name="lista_articulos"),
    url(r'^crear-articulo/$', CrearArticulo.as_view(), name='crear_articulo'),
    url(r'^(?P<slug>[-\w]+)/$', DetalleArticulo.as_view(),
        name="detalle_articulo"),
    url(r'^crear-categoria/$', CrearCategoria.as_view(),
        name='crear_categoria'),
]
