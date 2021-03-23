from django.core import mail
from selenium.webdriver.common.keys import Keys
import re

from .base import FunctionalTest

TEST_EMAIL = 'pipi@pupu.com'
SUBJECT = 'Tu enlace de entrada a Superlistas'


class LoginTest(FunctionalTest):

    def test_puede_ingresarse_con_el_link_de_email(self):
        self.browser.get(self.live_server_url)

        # completar campo email
        self.browser.find_element_by_name('email').send_keys(TEST_EMAIL)
        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)

        self.esperar_a(lambda: self.assertIn(
            'Busque en su email',
            self.browser.find_element_by_tag_name('body').text
        ))

        email = mail.outbox[0]
        self.assertIn(TEST_EMAIL, email.to)
        self.assertEqual(email.subject, SUBJECT)
        self.assertIn('Usá este enlace para entrar', email.body)
        url_search = re.search(r'http://.+/.+$', email.body)
        if not url_search:
            self.fail(
                f'No se encontró url en el cuerpo del mensaje:\n{email.body}')
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        self.browser.get(url)
        self.esperar_ingreso(email=TEST_EMAIL)

        self.browser.find_element_by_link_text('Salir').click()

        self.esperar_salida(email=TEST_EMAIL)
