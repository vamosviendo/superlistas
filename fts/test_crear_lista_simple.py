from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest
from .pag_lista import PagLista


class NewVisitorTest(FunctionalTest):

    def test_puede_comenzar_una_lista_y_recuperarla_mas_tarde(self):
        self.browser.get(self.live_server_url)

        # El título y el encabezado de la página mencionan listas de tareas
        self.assertIn('tareas', self.browser.title)
        texto_encabezado = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('tareas', texto_encabezado)

        # Inmediatamente después hay una invitación a ingresar tareas
        pag_lista = PagLista(self)
        inputbox = pag_lista.buscar_campo_de_entrada_item()
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Ingrese una tarea'
        )
        inputbox.send_keys('Hacer las compras')
        inputbox.send_keys(Keys.ENTER)

        pag_lista.esperar_fila_en_tabla_lista('Hacer las compras', 1)

        inputbox = pag_lista.buscar_campo_de_entrada_item()
        inputbox.send_keys('Guardar las vituallas')
        inputbox.send_keys(Keys.ENTER)

        pag_lista.esperar_fila_en_tabla_lista('Hacer las compras', 1)
        pag_lista.esperar_fila_en_tabla_lista('Guardar las vituallas', 2)

    def test_distintos_usuarios_pueden_empezar_listas_en_distintas_urls(self):

        # La usuaria Edith inicia una lista
        self.browser.get(self.live_server_url)
        pag_lista = PagLista(self)
        inputbox = pag_lista.buscar_campo_de_entrada_item()
        inputbox.send_keys('Hacer las compras')
        inputbox.send_keys(Keys.ENTER)
        pag_lista.esperar_fila_en_tabla_lista('Hacer las compras', 1)

        url_lista_edith = self.browser.current_url
        self.assertRegex(url_lista_edith, '/listas/.+')

        # La usuaria Edith abandona el sitio. El usuario Francis ingresa al
        # sitio.
        self.browser.quit()
        self.browser = webdriver.Firefox(log_path=self.logpath)
        self.browser.get(self.live_server_url)

        # No hay rastros de la lista de Edith
        texto_pag = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Hacer las compras', texto_pag)
        self.assertNotIn('vituallas', texto_pag)

        # Francis da inicio a una nueva lista
        inputbox = pag_lista.buscar_campo_de_entrada_item()
        inputbox.send_keys('Cortar el pasto')
        inputbox.send_keys(Keys.ENTER)
        pag_lista.esperar_fila_en_tabla_lista('Cortar el pasto', 1)

        # Francis tiene su propia URL única
        url_lista_francis = self.browser.current_url
        self.assertRegex(url_lista_francis, '/listas/.+')
        self.assertNotEqual(url_lista_francis, url_lista_edith)

        # Una vez más, no hay rastros de la lista de Edith
        texto_pag = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Hacer las compras', texto_pag)
        self.assertIn('Cortar el pasto', texto_pag)
