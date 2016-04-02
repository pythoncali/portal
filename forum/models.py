from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from taggit.managers import TaggableManager
from django.conf import settings
from django.core.exceptions import ValidationError
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
    # Introduje un par de lineas como ideas sueltas para no perder la idea.
    # pero esto requiere añadir un campo al modelo. ¿Hay alguna otra forma?

    def get_unanswered(self):
        return Pregunta.objects.filter(tiene_respuesta=False)

    def get_answered(self):
        return Pregunta.objects.filter(tiene_respuesta=True)


class Comentario(models.Model):
    '''Modelo para alojar los diferentes comentarios hechos en el foro, los
    cuales se supone seran para complementar diferentes aspectos de la pregunta
    o respuesta sobre la cual se hacen.'''
    creado_en = models.DateTimeField(auto_now_add=True, editable=False)
    modificado_en = models.DateTimeField(auto_now=True)
    comentador = models.ForeignKey(settings.AUTH_USER_MODEL)
    comentario = models.TextField(max_length=3000, blank=True)

    class Meta:
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'
        ordering = ('-creado_en',)


class Votos(models.Model):
    '''Modelo para llevar el registro de votos aplicados a los registros de los
    otros dos modelos. La idea principal es llevar un registro de
    transaccionalidad, para registrar adecuadamente un voto, positivo o
    negativo en el caso de las respuestas, o positivo unicamente en el caso de
    las preguntas.
    '''
    creado_en = models.DateTimeField(auto_now_add=True, editable=False)
    modificado_en = models.DateTimeField(auto_now=True)
    votante = models.ForeignKey(settings.AUTH_USER_MODEL)
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
    vistas = models.IntegerField(default=0)
    tags = TaggableManager(blank=True)
    objects = ForoManager()

    class Meta:
        verbose_name = 'Pregunta'
        verbose_name_plural = 'Preguntas'
        ordering = ('tiene_respuesta', '-vistas', '-creado_en',)

    def __str__(self):
        return self.titulo

    def incrementar_vistas(self):
        self.vistas += 1
        self.save()

    def get_answers_count(self):
        return self.respuesta_set.all().count()

    def get_accepted_answer(self):
        try:
            return self.respuesta_set.get(aceptada=True)
        except ObjectDoesNotExist:
            return "Quien hizó la pregunta, aun no ha marcado ninguna respuesta como aceptada."

    def get_answers(self):
        return self.respuesta_set.all()

    def voto(self, voto, votante):
        if votante == self.autor:
            raise ValidationError("Lo sentimos, no puedes votar por tu propia pregunta")

        else:
            self.votos.create(voto=voto, votante=votante)

    def calcular_votos(self):
        up_votos = self.votos.filter(voto=1).count()
        down_votos = self.votos.filter(voto=-1).count()
        votacion = up_votos - down_votos
        return votacion


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
    aceptada = models.BooleanField(default=False)
    votos = models.ManyToManyField(Votos, blank=True, limit_choices_to={'pk': 0})
    tags = TaggableManager(blank=True)
    objects = ForoManager()

    class Meta:
        verbose_name = 'Respuesta'
        verbose_name_plural = 'Respuestas'
        ordering = ('-aceptada', '-creado_en',)

    def voto(self, voto, votante):
        if votante == self.autor:
            raise ValidationError("Lo sentimos, no puedes votar por tu propia pregunta")

        else:
            self.votos.create(voto=voto, votante=votante)

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
        up_votos = self.votos.filter(voto=1).count()
        down_votos = self.votos.filter(voto=-1).count()
        votacion = up_votos - down_votos
        return votacion

    def __str__(self):
        return self.descripcion
