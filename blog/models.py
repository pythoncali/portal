from django.db import models
from taggit.managers import TaggableManager
from autoslug import AutoSlugField
from django.conf import settings

"""
## TODO ##
1. Como el direccionamiento estara ligado al uso de slugs, tanto en el caso de
las categorias como de las entradas,es necesario encontrar una manera de poder
conservar la validez de los enlaces, aun cuando el campo slug sea modificado
porque se cambio el titulo de la entrada o el nombre de la categoria.
2. Es importante incluir una manera mucho mas efectiva de incluir una imagen en
las entradas, hasta ahora es muy precaria la manera en que esta siendo usada.
3. ¿Como añadir la funcionalidad de los comentarios a las entradas? Ademas
considerar la posibilidad que esos comentarios puedan ser validados por el
autor o por un administrador del sistema, para evitar comentarios innecesarios
o poco validos para el uso de la comunidad.
"""


class Categoria(models.Model):
    """Clase que define el modelo para la creacion de categorias que permitan
    clasificar con mayor facilidad las diferentes publicaciones escritas en el
    blog de la comunidad
    """
    creado_en = models.DateTimeField(auto_now_add=True)
    modificado_en = models.DateTimeField(auto_now=True)
    nombre = models.CharField(max_length=20, unique=True, null=False)
    slug = AutoSlugField(populate_from='nombre', unique=True, editable=False)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ('nombre',)

    def __str__(self):
        return self.nombre


class ArticuloManager(models.Manager):
    """Manager para la clase Articulo, contiene algunas de las funcionalidades
    frecuentes de los modelos, siguiendo el lineamiento de usar una estructura
    mas robusta en los modelos."""

    def get_published(self):
        """Metodo para garantizar que siempre se muestren unicamente los
        articulos que ya han sido publicados por los autores en el blog.
        """
        articulo = Articulo.objects.filter(estado='p')
        return articulo

    def get_drafts(self):
        """Metodo con el fin de invocar los articulos en estado de borrador
        """
        articulo = Articulo.objects.filter(estado='b')
        return articulo


class Articulo(models.Model):
    """Clase para definir el modelo y estructura de las publicaciones del
    portal
    """
    ESTADO = (
        ('b', 'borrador'),
        ('p', 'publicado'),
    )
    creado_en = models.DateTimeField(auto_now_add=True, editable=False)
    modificado_en = models.DateTimeField(auto_now=True)
    titulo = models.CharField(max_length=50, null=False, unique=True)
    imagen_destacada = models.ImageField(upload_to='articulos/', null=True,
                                         blank=True)
    contenido = models.TextField(null=False)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL)
    categoria = models.ForeignKey(Categoria)
    tags = TaggableManager()
    slug = AutoSlugField(populate_from='titulo', unique=True, editable=False)
    estado = models.CharField(max_length=1, choices=ESTADO, default='b')
    objects = ArticuloManager()

    class Meta:
        verbose_name = "Articulo"
        verbose_name_plural = "Articulos"
        ordering = ('-creado_en',)

    def __str__(self):
        return self.titulo
