from django.views.generic import ListView, DetailView, CreateView
from braces.views import LoginRequiredMixin
from .models import Articulo, Categoria

"""
## TODO ##
1. Hace falta la vista que permita editar los articulos creados para que sean
actualizados.
2. Hace falta crear vistas para CRUD de las categorias.
3. Crear mensajes de advertencia sobre el resultado de realizar cualquier
actividad de CRUD de cada una de las vistas, cada vez que haya una llamada a
'success_url' en cualquiera de las vistas.
"""


class ListaArticulos(ListView):
    """Vista usando concepto de 'Class Based Views' para llamar todos los
    articulos, asi se habilita la opcion de permitir acceso a las
    funcionalidades del portal, sin necesidad de dar acceso al lado
    administrativo del mismo.
    """
    model = Articulo
    queryset = Articulo.objects.get_published()
    paginate_by = 10
    context_object_name = 'lista_articulos'


class DetalleArticulo(DetailView):
    """Vista usando concepto de 'Class Based Views' para llamar un articulo,
    asi se habilita la opcion de permitir acceso a las funcionalidades del
    portal, sin necesidad de dar acceso al lado administrativo del mismo.
    """
    model = Articulo
    context_obj_name = 'articulo'


class CrearArticulo(LoginRequiredMixin, CreateView):
    """Vista usando concepto de 'Class Based Views' para crear un articulo,
    asi se habilita la opcion de permitir acceso a las funcionalidades del
    portal, sin necesidad de dar acceso al lado administrativo del mismo.
    """
    model = Articulo
    success_url = '/blog/'
    fields = ['titulo', 'imagen_destacada', 'contenido', 'categoria', 'autor',
              'tags', 'estado']


class ListaCategorias(ListView):
    """Vista usando concepto de 'Class Based Views' para llamar todas los
    categorias, asi se habilita la opcion de permitir acceso a las
    funcionalidades del portal, sin necesidad de dar acceso al lado
    administrativo del mismo.
    """
    model = Categoria
    context_object_name = 'lista_categorias'


class CrearCategoria(LoginRequiredMixin, CreateView):
    """Vista usando concepto de 'Class Based Views' para crear una categoria,
    asi se habilita la opcion de permitir acceso a las funcionalidades del
    portal, sin necesidad de dar acceso al lado administrativo del mismo.
    """
    model = Categoria
    success_url = '/blog/categorias/'
    fields = ['nombre', ]
