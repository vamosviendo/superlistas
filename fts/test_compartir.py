from selenium import webdriver

from .base import FunctionalTest
from .pag_lista import PagLista


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