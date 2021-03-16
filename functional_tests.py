from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_puede_comenzar_una_lista_y_recuperarla_mas_tarde(self):
        self.browser.get('http://localhost:8000')

        self.assertIn('tareas', self.browser.title)
        self.fail('Terminar el test!')


if __name__ == '__main__':
    unittest.main()
