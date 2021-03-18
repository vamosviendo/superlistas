import os
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys


MAX_WAIT = 5


class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server

    def tearDown(self):
        self.browser.quit()

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

    def test_puede_comenzar_una_lista_y_recuperarla_mas_tarde(self):
        self.browser.get(self.live_server_url)

        # El título y el encabezado de la página mencionan listas de tareas
        self.assertIn('tareas', self.browser.title)
        texto_encabezado = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('tareas', texto_encabezado)

        # Inmediatamente después hay una invitación a ingresar tareas
        inputbox = self.browser.find_element_by_id('id_item_nuevo')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Ingrese una tarea'
        )
        inputbox.send_keys('Hacer las compras')
        inputbox.send_keys(Keys.ENTER)

        self.esperar_fila_en_tabla_lista('1: Hacer las compras')

        inputbox = self.browser.find_element_by_id('id_item_nuevo')
        inputbox.send_keys('Guardar las vituallas')
        inputbox.send_keys(Keys.ENTER)

        self.esperar_fila_en_tabla_lista('1: Hacer las compras')
        self.esperar_fila_en_tabla_lista('2: Guardar las vituallas')

    def test_distintos_usuarios_pueden_empezar_listas_en_distintas_urls(self):

        # La usuaria Edith inicia una lista
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_item_nuevo')
        inputbox.send_keys('Hacer las compras')
        inputbox.send_keys(Keys.ENTER)
        self.esperar_fila_en_tabla_lista('1: Hacer las compras')

        url_lista_edith = self.browser.current_url
        self.assertRegex(url_lista_edith, '/listas/.+')

        # La usuaria Edith abandona el sitio. El usuario Francis ingresa al
        # sitio.
        self.browser.quit()
        self.browser = webdriver.Firefox()
        self.browser.get(self.live_server_url)

        # No hay rastros de la lista de Edith
        texto_pag = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Hacer las compras', texto_pag)
        self.assertNotIn('vituallas', texto_pag)

        # Francis da inicio a una nueva lista
        inputbox = self.browser.find_element_by_id('id_item_nuevo')
        inputbox.send_keys('Cortar el pasto')
        inputbox.send_keys(Keys.ENTER)
        self.esperar_fila_en_tabla_lista('1: Cortar el pasto')

        # Francis tiene su propia URL única
        url_lista_francis = self.browser.current_url
        self.assertRegex(url_lista_francis, '/listas/.+')
        self.assertNotEqual(url_lista_francis, url_lista_edith)

        # Una vez más, no hay rastros de la lista de Edith
        texto_pag = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Hacer las compras', texto_pag)
        self.assertIn('Cortar el pasto', texto_pag)

    def test_distribucion_y_estilo(self):
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # El campo inputbox debe estar centrado en la página
        inputbox = self.browser.find_element_by_id('id_item_nuevo')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )

        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.esperar_fila_en_tabla_lista('1: testing')
        inputbox = self.browser.find_element_by_id('id_item_nuevo')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )
