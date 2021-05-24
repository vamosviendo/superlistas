from fts.base import FunctionalTest
from fts.pag_lista import PagLista


class MisListasTest(FunctionalTest):

    def test_listas_de_usuario_logueado_se_guardan_como_llmis_listasll(self):

        self.crear_sesion_preautenticada('pipi@pupu.com')
        self.browser.get(self.live_server_url)
        pag_lista = PagLista(self)
        pag_lista.agregar_item_a_lista('Reticulate splines')
        pag_lista.agregar_item_a_lista('Immanentize eschaton')
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
        pag_lista.agregar_item_a_lista('Click cows')
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
