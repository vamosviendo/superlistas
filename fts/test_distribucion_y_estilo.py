from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class DyETest(FunctionalTest):

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
