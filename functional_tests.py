import time
import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_puede_comenzar_una_lista_y_recuperarla_mas_tarde(self):
        self.browser.get('http://localhost:8000')

        # El título y el encabezado de la página mencionan listas de tareas
        self.assertIn('tareas', self.browser.title)
        texto_encabezado = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('tareas', texto_encabezado)

        # Inmediatamente después hay una invitación a ingresar tareas
        inputbox = self.browser.find_element_by_id('id_item_nuevo')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Ingrese una tarea'
        )
        inputbox.send_keys('Hacer las compras')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        tabla = self.browser.find_element_by_id('id_tabla_lista')
        filas = tabla.find_elements_by_tag_name('tr')
        self.assertIn('1: Hacer las compras', [fila.text for fila in filas])

        inputbox = self.browser.find_element_by_id('id_item_nuevo')
        inputbox.send_keys('Guardar las vituallas')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        tabla = self.browser.find_element_by_id('id_tabla_lista')
        filas = tabla.find_elements_by_tag_name('tr')
        self.assertIn('1: Hacer las compras', [fila.text for fila in filas])
        self.assertIn('2: Guardar las vituallas', [fila.text for fila in filas])

        self.fail('Terminar el test!')


if __name__ == '__main__':
    unittest.main()
