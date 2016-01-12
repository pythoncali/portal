from django.conf.urls import url
from .views import (DetalleArticulo, CrearArticulo, CrearCategoria,
                    ListaCategorias, blog_list)


urlpatterns = [
    url(r'^$', blog_list, name="lista_articulos"),
    url(r'^crear-articulo/$', CrearArticulo.as_view(), name='crear_articulo'),
    url(r'^crear-categoria/$', CrearCategoria.as_view(),
        name='crear_categoria'),
    url(r'^categorias/$', ListaCategorias.as_view(),
        name="lista_categorias"),
    url(r'^entradas/(?P<slug>[-\w]+)/$', DetalleArticulo.as_view(),
        name="detalle_articulo"),
]
