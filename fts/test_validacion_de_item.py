from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class ValidacionItemsTest(FunctionalTest):

    def test_no_se_puede_agregar_items_vacios_a_la_lista(self):

        self.browser.get(self.live_server_url)
        self.buscar_campo_de_entrada_item().send_keys(Keys.ENTER)

        self.esperar_a(lambda:
            self.browser.find_element_by_css_selector('#id_texto:invalid'))

        self.buscar_campo_de_entrada_item().send_keys('comprar')
        self.esperar_a(lambda: self.browser.find_element_by_css_selector(
            "#id_texto:valid"))
        self.buscar_campo_de_entrada_item().send_keys(Keys.ENTER)
        self.esperar_fila_en_tabla_lista('1: comprar')

        self.buscar_campo_de_entrada_item().send_keys(Keys.ENTER)

        self.esperar_fila_en_tabla_lista('1: comprar')
        self.esperar_a(lambda: self.browser.find_element_by_css_selector(
            '#id_texto:invalid'))

        self.buscar_campo_de_entrada_item().send_keys('hacer té')
        self.esperar_a(lambda: self.browser.find_element_by_css_selector(
            "#id_texto:valid"))
        self.buscar_campo_de_entrada_item().send_keys(Keys.ENTER)
        self.esperar_fila_en_tabla_lista('1: comprar')
        self.esperar_fila_en_tabla_lista('2: hacer té')

    def test_no_puede_agregarse_item_duplicado(self):
        self.browser.get(self.live_server_url)
        self.buscar_campo_de_entrada_item().send_keys('hacer compritas')
        self.buscar_campo_de_entrada_item().send_keys(Keys.ENTER)
        self.esperar_fila_en_tabla_lista('1: hacer compritas')

        self.buscar_campo_de_entrada_item().send_keys('hacer compritas')
        self.buscar_campo_de_entrada_item().send_keys(Keys.ENTER)
        self.esperar_a(
            lambda: self.assertEqual(
                self.browser.find_element_by_css_selector('.has-error').text,
                "Ya existe ese item en la lista"
            )
        )
