from selenium.webdriver.common.keys import Keys
from .base import espera


class PagLista:

    def __init__(self, test):
        self.test = test

    def obtener_filas_de_tabla(self):
        return self.test.browser.find_elements_by_css_selector(
            "#id_tabla_lista tr")

    @espera
    def esperar_fila_en_tabla_lista(self, texto_item, nro_item):
        texto_esperado_en_fila = f'{nro_item}: {texto_item}'
        filas = self.obtener_filas_de_tabla()
        self.test.assertIn(
            texto_esperado_en_fila,
            [fila.text for fila in filas]
        )

    def buscar_campo_de_entrada_item(self):
        return self.test.browser.find_element_by_id('id_texto')

    def agregar_item_a_lista(self, texto_item):
        nro_item_nuevo = len(self.obtener_filas_de_tabla()) + 1
        self.buscar_campo_de_entrada_item().send_keys(texto_item)
        self.buscar_campo_de_entrada_item().send_keys(Keys.ENTER)
        self.esperar_fila_en_tabla_lista(texto_item, nro_item_nuevo)
        return self

    def obtener_share_box(self):
        return self.test.browser.find_element_by_css_selector(
            'input[name="sharee"]')

    def obtener_lista_compartido_con(self):
        return self.test.browser.find_elements_by_css_selector('.list-sharee')

    def compartir_lista_con(self, email):
        self.obtener_share_box().send_keys(email)
        self.obtener_share_box().send_keys(Keys.ENTER)
        self.test.esperar_a(
            lambda: self.test.assertIn(
                email,
                [item.text for item in self.obtener_lista_compartido_con()]
            )
        )

    def obtener_duenio_de_lista(self):
        return self.test.browser.find_element_by_id('id_duenio_lista').text