from selenium import webdriver

from .base import FunctionalTest
from .pag_lista import PagLista
from .pag_mis_listas import PagMisListas


def quit_if_possible(browser):
    try:
        browser.quit()
    except:
        pass


class SharingTest(FunctionalTest):

    def test_puede_compartir_lista_con_otro_usuario(self):
        self.crear_sesion_preautenticada('edith@example.com')
        edith_browser = self.browser
        self.addCleanup(lambda: quit_if_possible(edith_browser))

        oni_browser = webdriver.Firefox(log_path=self.logpath)
        self.addCleanup(lambda: quit_if_possible(oni_browser))
        self.browser = oni_browser
        self.crear_sesion_preautenticada('oniciferous@example.com')

        self.browser = edith_browser
        self.browser.get(self.live_server_url)
        pag_lista = PagLista(self).agregar_item_a_lista('Conseguir ayuda')

        share_box = pag_lista.obtener_share_box()
        self.assertEqual(
            share_box.get_attribute('placeholder'),
            'su-amigo@ejemploc.com'
        )

        pag_lista.compartir_lista_con('oniciferous@example.com')

        self.browser = oni_browser
        PagMisListas(self).ir_a_pag_mis_listas()

        self.esperar_a(
            lambda: self.assertEqual(
                pag_lista.obtener_duenio_de_lista(),
                'edith@example.com'
            )
        )
        pag_lista.agregar_item_a_lista('Hola Edith!')

        self.browser = edith_browser
        self.browser.refresh()
        pag_lista.esperar_fila_en_tabla_lista('Hola Edith!', 2)