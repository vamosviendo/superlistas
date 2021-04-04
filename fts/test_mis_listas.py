from django.conf import settings
from selenium.webdriver.common.keys import Keys

from fts.base import FunctionalTest
from fts.server_tools import crear_sesion_en_server
from fts.management.commands.create_session import crear_sesion_preautenticada


class MisListasTest(FunctionalTest):

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

    def agregar_item_a_lista(self, texto_item):
        num_filas = len(self.browser.find_elements_by_css_selector('#id_tabla_lista tr'))
        self.buscar_campo_de_entrada_item().send_keys(texto_item)
        self.buscar_campo_de_entrada_item().send_keys(Keys.ENTER)
        nro_item = num_filas + 1
        self.esperar_fila_en_tabla_lista(f'{nro_item}: {texto_item}')

    def test_listas_de_usuario_logueado_se_guardan_como_llmis_listasll(self):

        self.crear_sesion_preautenticada('pipi@pupu.com')
        self.browser.get(self.live_server_url)
        self.agregar_item_a_lista('Reticulate splines')
        self.agregar_item_a_lista('Immanentize eschaton')
        url_primera_lista = self.browser.current_url

        self.browser.find_element_by_link_text('Mis listas').click()

        self.esperar_a(
            lambda: self.browser.find_element_by_link_text('Reticulate splines')
        )
        self.browser.find_element_by_link_text('Reticulate splines').click()
        self.esperar_a(
            lambda: self.assertEqual(self.browser.current_url,
                                     url_primera_lista)
        )

        # Comenzar otra lista
        self.browser.get(self.live_server_url)
        self.agregar_item_a_lista('Click cows')
        url_segunda_lista = self.browser.current_url

        # Aparece una segunda lista debajo de "mis listas"
        self.browser.find_element_by_link_text('Mis listas').click()
        self.esperar_a(
            lambda: self.browser.find_element_by_link_text('Click cows')
        )
        self.browser.find_element_by_link_text('Click cows').click()
        self.esperar_a(
            lambda: self.assertEqual(
                self.browser.current_url, url_segunda_lista)
        )

        # Al desloguearse, la opción "Mis listas" desaparece
        self.browser.find_element_by_link_text('Salir').click()
        self.esperar_a(
            lambda: self.assertEqual(
                self.browser.find_elements_by_link_text('Mis listas'),
                []
            )
        )
