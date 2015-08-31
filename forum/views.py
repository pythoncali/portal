from django.views.generic import ListView, DetailView, CreateView
from braces.views import LoginRequiredMixin
from .models import Pregunta, Respuesta


class CrearPregunta(LoginRequiredMixin, CreateView):
    model = Pregunta


class CrearRespuesta(LoginRequiredMixin, CreateView):
    model = Respuesta


class ListaPreguntas(ListView):
    model = Pregunta
    paginate_by = 10


class ListaRespuestas(ListView):
    model = Respuesta


class DetallePregunta(DetailView):
    model = Pregunta


class DetalleRespuesta(DetailView):
    model = Respuesta
