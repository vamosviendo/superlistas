from django.urls import resolve
from django.test import TestCase

from listas.models import Item
from listas.views import home_page


class HomePageTest(TestCase):

    def test_url_raiz_resuelve_a_vista_home_page(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_devuelve_html_correcto(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_puede_salvar_un_request_POST(self):
        response = self.client.post('/', data={'texto_item': 'Nuevo item'})
        self.assertIn('Nuevo item', response.content.decode())
        self.assertTemplateUsed(response, 'home.html')


class ItemModelTest(TestCase):

    def test_salvar_y_recuperar_items(self):
        primer_item = Item()
        primer_item.text = 'El primer item de la lista'
        primer_item.save()

        segundo_item = Item()
        segundo_item.text = 'Segundo item'
        segundo_item.save()

        items_guardados = Item.objects.all()
        self.assertEqual(items_guardados.count(), 2)

        primer_item_guardado = items_guardados[0]
        segundo_item_guardado = items_guardados[1]
        self.assertEqual(
            primer_item_guardado.text, 'El primer item de la lista')
        self.assertEqual(segundo_item_guardado.text, 'Segundo item')
