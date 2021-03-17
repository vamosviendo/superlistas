from django.urls import resolve
from django.test import TestCase
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
