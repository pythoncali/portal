from django.test import TestCase

from .models import Pregunta, Respuesta
from model_mommy import mommy


def gen_func():
    return 'this-is-an-sluged-example'


class TestModels(TestCase):

    def test_model_pregunta(self):
        pregunta = mommy.make(Pregunta)
        self.assertTrue(isinstance(pregunta, Pregunta))
        self.assertEqual(pregunta.__str__(), pregunta.titulo)
        self.assertEqual(pregunta.slug, gen_func())
        self.assertNotEqual(pregunta.creado_en, pregunta.modificado_en)

    def test_model_respuesta(self):
        respuesta = mommy.make(Respuesta)
        self.assertTrue(isinstance(respuesta, Respuesta))
        self.assertEqual(respuesta.__str__(), respuesta.descripcion)
        self.assertEqual(respuesta.slug, gen_func())
        self.assertNotEqual(respuesta.creado_en, respuesta.modificado_en)

    def test_manager(self):
        pregunta = mommy.make(Pregunta)
        self.assertFalse(Pregunta.objects.get_unanswered_questions())
        self.assertFalse(Pregunta.objects.get_answered_questions())
        self.assertFalse(Pregunta.objects.get_questions_answers())
        self.assertFalse(Pregunta.objects.get_answers(), pregunta.titulo)
