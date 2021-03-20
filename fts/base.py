import os
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.common.exceptions import WebDriverException


MAX_WAIT = 10


class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server

    def tearDown(self):
        self.browser.quit()

    def esperar_a(self, fn):
        inicio = time.time()
        while True:
            try:
                return fn()
            except (AssertionError, WebDriverException) as e:
                if time.time() - inicio > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def esperar_fila_en_tabla_lista(self, texto_fila):
        inicio = time.time()
        while True:
            try:
                tabla = self.browser.find_element_by_id('id_tabla_lista')
                filas = tabla.find_elements_by_tag_name('tr')
                self.assertIn(texto_fila, [fila.text for fila in filas])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - inicio > MAX_WAIT:
                    raise e
                time.sleep(0.5)
