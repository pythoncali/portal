from django.views.generic import ListView, DetailView, CreateView
from django.core.urlresolvers import reverse_lazy, reverse
from braces.views import LoginRequiredMixin
from .models import Pregunta, Respuesta, ComentarioPregunta, ComentarioRespuesta


class CrearPregunta(LoginRequiredMixin, CreateView):
    '''Vista usando concepto de 'Class Based Views' para registrar y publicar,
    una pregunta de forma abierta en el foro, habilitando creacion de preguntas
    sin necesidad de dar acceso al lado administrativo del portal.
    '''
    model = Pregunta
    success_url = reverse_lazy('lista_preguntas')
    fields = ['titulo', 'descripcion', 'tags']

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super(CrearPregunta, self).form_valid(form)


class CrearRespuesta(LoginRequiredMixin, CreateView):
    model = Respuesta
    fields = ['descripcion', 'tags']

    def form_valid(self, form):
        form.instance.autor = self.request.user
        form.instance.pregunta_id = self.kwargs['pregunta_id']
        return super(CrearRespuesta, self).form_valid(form)

    def get_success_url(self):
        slug = Pregunta.objects.get(id=self.kwargs['pregunta_id']).slug
        return reverse('detalle_pregunta', kwargs={'slug': slug})


class ComentarPregunta(LoginRequiredMixin, CreateView):
    template_name = 'forum/comentario_form.html'
    model = ComentarioPregunta
    fields = ['comentario', ]

    def form_valid(self, form):
        form.instance.comentador = self.request.user
        form.instance.pregunta_id = self.kwargs['pregunta_id']
        return super(ComentarPregunta, self).form_valid(form)

    def get_success_url(self):
        slug = Pregunta.objects.get(id=self.kwargs['pregunta_id']).slug
        return reverse('detalle_pregunta', kwargs={'slug': slug})


class ComentarRespuesta(LoginRequiredMixin, CreateView):
    template_name = 'forum/comentario_form.html'
    model = ComentarioRespuesta
    fields = ['comentario', ]

    def form_valid(self, form):
        form.instance.comentador = self.request.user
        form.instance.respuesta_id = self.kwargs['respuesta_id']
        return super(ComentarRespuesta, self).form_valid(form)

    def get_success_url(self):
        respuesta = Respuesta.objects.get(id=self.kwargs['respuesta_id'])
        slug = respuesta.pregunta.slug
        return reverse('detalle_pregunta', kwargs={'slug': slug})


class ListaPreguntas(ListView):
    model = Pregunta
    paginate_by = 10
    context_object_name = 'lista_preguntas'


class ListaRespuestas(ListView):
    model = Respuesta


class DetallePregunta(DetailView):
    model = Pregunta
    context_object_name = 'pregunta'

    def get_object(self):
        # Call the superclass
        pregunta = super(DetallePregunta, self).get_object()
        pregunta.incrementar_vistas()
        return pregunta


class DetalleRespuesta(DetailView):
    model = Respuesta
