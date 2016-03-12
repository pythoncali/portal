from django.test import TestCase
from django.core.urlresolvers import reverse
from .models import Articulo, Categoria

from model_mommy import mommy


def gen_func():
    return 'this-is-an-sluged-example'


class TestModels(TestCase):

    def setUp(self):
        self.articulo = mommy.make(Articulo)
        self.articulo_p = mommy.make(Articulo, estado="p")
        self.categoria = mommy.make(Categoria)

    def test_model_articulo(self):

        self.assertTrue(isinstance(self.articulo, Articulo))
        self.assertEqual(self.articulo.__str__(), self.articulo.titulo)
        self.assertEqual(self.articulo.slug, gen_func())
        self.assertNotEqual(self.articulo.creado_en, self.articulo.modificado_en)

    def test_model_categoria(self):
        self.assertTrue(isinstance(self.categoria, Categoria))
        self.assertEqual(self.categoria.__str__(), self.categoria.nombre)

    def test_articulo_drafts(self):
        self.assertTrue(Articulo.objects.get_drafts())
        self.assertEqual(
            Articulo.objects.get_drafts()[0].titulo, self.articulo.titulo)

    def test_articulo_published(self):
        self.assertTrue(Articulo.objects.get_published())
        self.assertEqual(
            Articulo.objects.get_published()[0].titulo, self.articulo_p.titulo)


class TestViews(TestCase):

    def setUp(self):
        self.art_uno = mommy.make(Articulo, estado="p")
        self.art_dos = mommy.make(Articulo, estado="p")

    def test_lista_articulos(self):
        url = reverse('lista_articulos')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(
            self.art_uno.categoria, self.art_dos.categoria in resp.context[
                "categorias_list"])

    def test_detalle_articulo(self):
        url_uno = reverse('detalle_articulo', args=[self.art_uno.slug])
        resp_uno = self.client.get(url_uno)
        self.assertEqual(resp_uno.status_code, 200)
        self.assertTrue(
            self.art_uno.titulo in resp_uno.context["articulo"].__str__())
        url_dos = reverse('detalle_articulo', args=[self.art_dos.slug])
        resp_dos = self.client.get(url_dos)
        self.assertEqual(resp_dos.status_code, 200)
        self.assertTrue(
            self.art_dos.titulo in resp_dos.context["articulo"].__str__())

    def test_lista_categorias(self):
        url = reverse('lista_categorias')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(
            self.art_uno.categoria, self.art_dos.categoria in resp.context[
                "lista_categorias"])
