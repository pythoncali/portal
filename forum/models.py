from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from taggit.managers import TaggableManager
from django.conf import settings
from autoslug import AutoSlugField
# import user

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
    # Introduje un par de lineas como ideas sueltas para no perder la idea.
    # pero esto requiere añadir un campo al modelo. ¿Hay alguna otra forma?

    def get_unanswered(self):
        return Pregunta.objects.filter(tiene_respuesta=False)

    def get_answered(self):
        return Pregunta.objects.filter(tiene_respuesta=True)


class Votos(models.Model):
    '''Modelo para llevar el registro de votos aplicados a los registros de los
    otros dos modelos. La idea principal es llevar un registro de
    transaccionalidad, para registrar adecuadamente un voto, positivo o
    negativo en el caso de las respuestas, o positivo unicamente en el caso de
    las preguntas.
    '''
    creado_en = models.DateTimeField(auto_now_add=True, editable=False)
    modificado_en = models.DateTimeField(auto_now=True)
    voto = models.SmallIntegerField()

    class Meta:
        verbose_name = 'Voto'
        verbose_name_plural = 'Votos'


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
    tiene_respuesta = models.BooleanField(default=False)
    votos = models.ManyToManyField(Votos, blank=True, limit_choices_to={'pk': 0})
    tags = TaggableManager(blank=True)
    objects = ForoManager()

    class Meta:
        verbose_name = 'Pregunta'
        verbose_name_plural = 'Preguntas'
        ordering = ('-creado_en',)

    def __str__(self):
        return self.titulo

    def get_answers_count(self):
        return self.respuesta_set.all().count()

    def get_accepted_answer(self):
        try:
            return self.respuesta_set.get(aceptada=True)
        except ObjectDoesNotExist:
            return "Quien hizó la pregunta, aun no ha marcado ninguna respuesta como aceptada."

    def get_answers(self):
        return self.respuesta_set.all()

    def votar(self):
        self.votos.create(voto=1)


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
    slug = AutoSlugField(populate_from='descripcion', unique=True, editable=False)
    votos = models.ManyToManyField(Votos, blank=True, limit_choices_to={'pk': 0})
    tags = TaggableManager(blank=True)
    objects = ForoManager()

    class Meta:
        verbose_name = 'Respuesta'
        verbose_name_plural = 'Respuestas'
        ordering = ('-aceptada', 'creado_en',)

    def voto_positivo(self):
        self.votos.create(voto=1)

    def voto_negativo(self):
        self.votos.create(voto=-1)

    def aceptar_respuesta(self):
        self.pregunta.tiene_respuesta = False
        self.pregunta.save()
        for r in self.pregunta.get_answers():
            r.aceptada = False
            r.save()

        self.aceptada = True
        self.save()
        self.pregunta.tiene_respuesta = True
        self.pregunta.save()

    def calcular_votos(self):
        total_recibidos = self.votos.count()
        up_votos = self.votos.filter(voto=1).count()
        down_votos = self.votos.filter(voto=-1).count()
        votacion = up_votos - down_votos
        return (total_recibidos, votacion)

    def __str__(self):
        return self.descripcion
