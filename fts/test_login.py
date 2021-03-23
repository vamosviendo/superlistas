import os
import poplib
import re
import time

from django.core import mail
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest

SUBJECT = 'Tu enlace de entrada a Superlistas'


class LoginTest(FunctionalTest):

    def esperar_email(self, test_email, subject):
        if not self.staging_server:
            email = mail.outbox[0]
            self.assertIn(test_email, email.to)
            self.assertEqual(email.subject, subject)
            return email.body

        email_id = None
        inicio = time.time()
        inbox = poplib.POP3_SSL('pop.gmail.com')
        try:
            inbox.user(test_email)
            inbox.pass_(os.environ['GMAIL_PASSWORD'])
            while time.time - inicio < 60:
                # Obtener los 10 mensajes más nuevos
                cuenta, _ = inbox.stat()
                for i in reversed(range(max(1, cuenta-10), cuenta+1)):
                    print('obteniendo msj', i)
                    _, lineas, __ = inbox.retr(i)
                    lineas = [l.decode('utf8') for l in lineas]
                    if f'Subject: {subject}' in lineas:
                        email_id = i
                        body = '\n'.join(lineas)
                        return body
                time.sleep(5)
        finally:
            if email_id:
                inbox.dele(email_id)
            inbox.quit()

    def test_puede_ingresarse_con_el_link_de_email(self):
        print(os.environ)
        if self.staging_server:
            test_email = 'htejedor@gmail.com'
        else:
            test_email = 'pipi@pupu.com'

        self.browser.get(self.live_server_url)

        # completar campo email
        self.browser.find_element_by_name('email').send_keys(test_email)
        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)

        self.esperar_a(lambda: self.assertIn(
            'Busque en su email',
            self.browser.find_element_by_tag_name('body').text
        ))

        body = self.esperar_email(test_email, SUBJECT)
        self.assertIn('Usá este enlace para entrar', body)
        url_search = re.search(r'http://.+/.+$', body)
        if not url_search:
            self.fail(
                f'No se encontró url en el cuerpo del mensaje:\n{body}')
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        self.browser.get(url)
        self.esperar_ingreso(email=test_email)

        self.browser.find_element_by_link_text('Salir').click()

        self.esperar_salida(email=test_email)
