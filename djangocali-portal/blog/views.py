from django.views.generic import ListView, DetailView, CreateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext
from django.shortcuts import render_to_response
from braces.views import LoginRequiredMixin
from .models import Articulo, Categoria

"""
## TODO ##
1. Hace falta la vista que permita editar los articulos existentes.
2. Hace falta la vista que permita editar las categorias existentes
3. Crear mensajes de advertencia sobre el resultado de realizar cualquier
actividad de CRUD de cada una de las vistas, cada vez que haya una llamada a
'success_url' en cualquiera de las vistas.
4. Hace falta la vista que permita eliminar articulos.
5. Hace falta la vista que permita eliminar categorias.
6. Agregar a las vistas de una restriccion por permisos de acceso.
7. Crear una CBV para reemplazar la vista funcional blog_list. Muy seguramente
la clase base a implementar por compatibilidad conceptual seria un TemplateView
con modificacion del contexto.
"""


def blog_list(request):
    """Vista funcional para generar la pagina central de lblog, con el
    contenido global de las entradas y poder alimentar la plantilla con
    informacion complementaria relevante, adicionalmente se deja abierta la
    opcion de poder agregar mas informacion al contexto en el futuro con mayor
    facilidad."""
    categorias_list = Categoria.objects.all()
    articulos_list = Articulo.objects.get_published()
    categoria_count = Categoria.objects.all().count()
    articulo_count = Articulo.objects.all().count()
    paginator = Paginator(articulos_list, 10)
    page = request.GET.get('page')
    tags = []

    try:
        articulos = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        articulos = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        articulos = paginator.page(paginator.num_pages)

    for articulo in articulos_list:
        for tag in articulo.tags.all():
            if tag not in tags:
                tags.append(tag)

    context = RequestContext(request, {
        'categorias_list': categorias_list,
        'articulos': articulos,
        'categoria_count': categoria_count,
        'articulo_count': articulo_count,
        'tags': tags,
    })

    return render_to_response('blog/articulo_list.html', context)


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
    fields = ['titulo', 'imagen_destacada', 'contenido', 'categoria', 'tags',
              'estado']

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super(CrearArticulo, self).form_valid(form)


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
