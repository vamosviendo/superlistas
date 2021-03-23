import os
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.common.exceptions import WebDriverException

from fts.server_tools import reset_database


MAX_WAIT = 10


def espera(fn):

    def fn_modificada(*args, **kwargs):
        inicio = time.time()
        while True:
            try:
                return fn(*args, **kwargs)
            except (AssertionError, WebDriverException) as e:
                if time.time() - inicio > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    return fn_modificada


class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.staging_server = os.environ.get('STAGING_SERVER')
        if self.staging_server:
            self.live_server_url = 'http://' + self.staging_server
            reset_database(self.staging_server)

    def tearDown(self):
        self.browser.quit()

    @espera
    def esperar_a(self, fn):
        return fn()

    @espera
    def esperar_fila_en_tabla_lista(self, texto_fila):
        tabla = self.browser.find_element_by_id('id_tabla_lista')
        filas = tabla.find_elements_by_tag_name('tr')
        self.assertIn(texto_fila, [fila.text for fila in filas])

    @espera
    def esperar_ingreso(self, email):
        self.browser.find_element_by_link_text('Salir')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(email, navbar.text)

    @espera
    def esperar_salida(self, email):
        self.browser.find_element_by_name('email')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertNotIn(email, navbar.text)

    def buscar_campo_de_entrada_item(self):
        return self.browser.find_element_by_id('id_texto')
