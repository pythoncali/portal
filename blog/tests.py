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
