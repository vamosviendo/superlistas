from django.http import HttpRequest
from django.urls import resolve
from django.test import TestCase
from listas.views import home_page

class HomePageTest(TestCase):

    def test_url_raiz_resuelve_a_vista_home_page(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_devuelve_html_correcto(self):
        request = HttpRequest()
        response = home_page(request)
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>Listas de tareas</title>', html)
        self.assertTrue(html.endswith('</html>'))
