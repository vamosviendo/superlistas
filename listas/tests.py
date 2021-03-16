from django.urls import resolve
from django.test import TestCase
from listas.views import home_page

class HomePageTest(TestCase):

    def test_url_raiz_resuelve_a_vista_home_page(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)
