from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest
from .pag_lista import PagLista


class ValidacionItemsTest(FunctionalTest):

    def buscar_elemento_error(self):
        return self.browser.find_element_by_css_selector('.has-error')

    def test_no_se_puede_agregar_items_vacios_a_la_lista(self):

        self.browser.get(self.live_server_url)
        pag_lista = PagLista(self)
        pag_lista.buscar_campo_de_entrada_item().send_keys(Keys.ENTER)

        self.esperar_a(lambda:
            self.browser.find_element_by_css_selector('#id_texto:invalid'))

        pag_lista.buscar_campo_de_entrada_item().send_keys('comprar')
        self.esperar_a(lambda: self.browser.find_element_by_css_selector(
            "#id_texto:valid"))
        pag_lista.buscar_campo_de_entrada_item().send_keys(Keys.ENTER)
        pag_lista.esperar_fila_en_tabla_lista('comprar', 1)

        self.buscar_campo_de_entrada_item().send_keys(Keys.ENTER)

        pag_lista.esperar_fila_en_tabla_lista('comprar', 1)
        self.esperar_a(lambda: self.browser.find_element_by_css_selector(
            '#id_texto:invalid'))

        pag_lista.buscar_campo_de_entrada_item().send_keys('hacer té')
        self.esperar_a(lambda: self.browser.find_element_by_css_selector(
            "#id_texto:valid"))
        pag_lista.buscar_campo_de_entrada_item().send_keys(Keys.ENTER)
        pag_lista.esperar_fila_en_tabla_lista('comprar', 1)
        pag_lista.esperar_fila_en_tabla_lista('hacer té', 2)

    def test_no_puede_agregarse_item_duplicado(self):
        self.browser.get(self.live_server_url)
        pag_lista = PagLista(self)
        pag_lista.buscar_campo_de_entrada_item().send_keys('hacer compritas')
        pag_lista.buscar_campo_de_entrada_item().send_keys(Keys.ENTER)
        pag_lista.esperar_fila_en_tabla_lista('hacer compritas', 1)

        pag_lista.buscar_campo_de_entrada_item().send_keys('hacer compritas')
        pag_lista.buscar_campo_de_entrada_item().send_keys(Keys.ENTER)
        self.esperar_a(
            lambda: self.assertEqual(
                self.buscar_elemento_error().text,
                'Ya existe ese item en la lista'
            )
        )

    def test_mensajes_de_error_se_borran_al_teclear(self):
        pl = PagLista(self)
        self.browser.get(self.live_server_url)
        pl.buscar_campo_de_entrada_item().send_keys('Dormir')
        pl.buscar_campo_de_entrada_item().send_keys(Keys.ENTER)
        pl.esperar_fila_en_tabla_lista('Dormir', 1)
        pl.buscar_campo_de_entrada_item().send_keys('Dormir')
        pl.buscar_campo_de_entrada_item().send_keys(Keys.ENTER)

        self.esperar_a(lambda: self.assertTrue(
            self.buscar_elemento_error().is_displayed()
        ))

        pl.buscar_campo_de_entrada_item().send_keys('a')

        self.esperar_a(lambda: self.assertFalse(
            self.buscar_elemento_error().is_displayed()
        ))
