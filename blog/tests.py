from django.test import TestCase

from .models import Articulo, Categoria
from model_mommy import mommy


def gen_func():
    return 'this-is-an-sluged-example'


class TestModels(TestCase):

    def test_model_articulo(self):
        articulo = mommy.make(Articulo)
        self.assertTrue(isinstance(articulo, Articulo))
        self.assertEqual(articulo.__str__(), articulo.titulo)
        self.assertEqual(articulo.slug, gen_func())
        self.assertNotEqual(articulo.creado_en, articulo.modificado_en)

    def test_model_categoria(self):
        categoria = mommy.make(Categoria)
        self.assertTrue(isinstance(categoria, Categoria))
        self.assertEqual(categoria.__str__(), categoria.nombre)

    def test_articulo_drafts(self):
        articulo = mommy.make(Articulo)
        self.assertTrue(Articulo.objects.get_drafts())
        self.assertEqual(
            Articulo.objects.get_drafts()[0].titulo, articulo.titulo)

    def test_articulo_published(self):
        articulo = mommy.make(Articulo, estado="p")
        self.assertTrue(Articulo.objects.get_published())
        self.assertEqual(
            Articulo.objects.get_published()[0].titulo, articulo.titulo)
