from django.db import models
from taggit.managers import TaggableManager
from django.conf import settings
from autoslug import AutoSlugField

'''
La intencion basica del app es brindar un espacio del tipo Stack-Overflow donde
los integrantes de la comunidad tengan la posibilidad de exponer sus dudas, y
que la misma comunidad pueda contestar y aportar, con un debate sano y
constructivo.
'''


class ForoManager(models.Manager):
    '''Manager generico para los modelos del app, siguiendo los lineamientos de
    buenas practicas de Django, al separar las funcionalidades de los modelos y
    la interaccion con la base de datos.'''

    # Estoy poniendo las funciones vacias para planear las interacciones y
    # posteriormente definer la forma de interaccion.

    def get_unanswered_questions():
        pass

    def get_answered_questions():
        pass

    def get_questions_answers():
        pass

    def get_answers():
        pass


class Pregunta(models.Model):
    '''La meta es crear un espacio donde sea posible hacer una pregunta a la
    comunidad, y esta responda, apoyando a la construccion de conocimiento
    colaborativo.
    '''
    creado_en = models.DateTimeField(auto_now_add=True, editable=False)
    modificado_en = models.DateTimeField(auto_now=True)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL)
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(max_length=3000)
    slug = AutoSlugField(populate_from='titulo', unique=True, editable=False)
    tags = TaggableManager()
    objects = ForoManager()

    class Meta:
        verbose_name = 'Pregunta'
        verbose_name_plural = 'Preguntas'
        ordering = ('-creado_en',)

    def __str__(self):
        return self.titulo


class Respuesta(models.Model):
    '''Las respuestas seran calificadas por la misma comunidad, buscando con
    eso dar mayor visibilidad a aquellas mejores respuestas. Adicionalmente las
    respuestas podran ser aceptadas por el usuario que hizo la pregunta, para
    calificar esas respuestas y destacar las que adicionalmente funcionaron o
    clarificaron lo que se buscaba.
    '''
    creado_en = models.DateTimeField(auto_now_add=True, editable=False)
    modificado_en = models.DateTimeField(auto_now=True)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL)
    pregunta = models.ForeignKey(Pregunta)
    descripcion = models.TextField(max_length=2000)
    votos = models.IntegerField(default=0)
    aceptada = models.BooleanField(default=False)
    objects = ForoManager()

    class Meta:
        verbose_name = 'Respuesta'
        verbose_name_plural = 'Respuestas'
        ordering = ('-aceptada', '-votos', 'creado_en',)

    def __str__(self):
        return self.descripcion
