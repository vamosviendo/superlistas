import os
import time
from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys

from fts.server_tools import reset_database, crear_sesion_en_server
from fts.management.commands.create_session import crear_sesion_preautenticada


MAX_WAIT = 10

SCREEN_DUMP_LOCATION = Path(__file__).resolve().parent / 'screendumps'


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
        self.logpath = Path(os.environ.get('HOME')) / 'geckodriver.log'
        self.browser = webdriver.Firefox(log_path=self.logpath)
        self.staging_server = os.environ.get('STAGING_SERVER')
        if self.staging_server:
            self.live_server_url = 'http://' + self.staging_server
            reset_database(self.staging_server)

    def tearDown(self):
        if self._test_fallido():
            if not SCREEN_DUMP_LOCATION.exists():
                SCREEN_DUMP_LOCATION.mkdir()
            for ix, handle in enumerate(self.browser.window_handles):
                self._windowid = ix
                self.browser.switch_to.window(handle)
                self.tomar_foto()
                self.volcar_html()
        self.browser.quit()
        super().tearDown()

    def _test_fallido(self):
        return any(error for (method, error) in self._outcome.errors)

    def tomar_foto(self):
        filename = self._generar_nombre_archivo() + '.png'
        print('guardando foto en', filename)
        self.browser.get_screenshot_as_file(filename)

    def volcar_html(self):
        filename = self._generar_nombre_archivo() + '.html'
        print('volcando HTML de la página a', filename)
        with open(filename, 'w') as f:
            f.write(self.browser.page_source)

    def _generar_nombre_archivo(self):
        timestamp = datetime.now().isoformat().replace(':', '.')[:19]
        return f'{SCREEN_DUMP_LOCATION}/{self.__class__.__name__}.' \
               f'{self._testMethodName}-window{self._windowid}-{timestamp}'

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

    def agregar_item_a_lista(self, texto_item):
        num_filas = len(self.browser.find_elements_by_css_selector('#id_tabla_lista tr'))
        self.buscar_campo_de_entrada_item().send_keys(texto_item)
        self.buscar_campo_de_entrada_item().send_keys(Keys.ENTER)
        nro_item = num_filas + 1
        self.esperar_fila_en_tabla_lista(f'{nro_item}: {texto_item}')

    def crear_sesion_preautenticada(self, email):
        if self.staging_server:
            session_key = crear_sesion_en_server(self.staging_server, email)
        else:
            session_key = crear_sesion_preautenticada(email)

        self.browser.get(self.live_server_url + '/404_no_existe/')
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session_key,
            path='/',
        ))
