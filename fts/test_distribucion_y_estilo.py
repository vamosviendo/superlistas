from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest
from .pag_lista import PagLista


class DyETest(FunctionalTest):

    def test_distribucion_y_estilo(self):
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # El campo inputbox debe estar centrado en la página
        pl = PagLista(self)
        inputbox = pl.buscar_campo_de_entrada_item()
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )

        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        pl.esperar_fila_en_tabla_lista('testing', 1)
        inputbox = pl.buscar_campo_de_entrada_item()
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )
