from django.conf import settings

from fts.base import FunctionalTest
from fts.server_tools import crear_sesion_en_server
from fts.management.commands.create_session import crear_sesion_preautenticada


class MisListasTest(FunctionalTest):

    def crear_sesion_preautenticada(self, email):
        if self.staging_server:
            session_key = crear_sesion_en_server(self.staging_server, email)
        else:
            session_key = crear_sesion_preautenticada(email)

        self.browser.get(self.live_server_url + '/404_no_existe/')
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session_key,
            path='/',
        ))

    def test_listas_de_usuario_logueado_se_guardan_como_llmis_listasll(self):
        email = 'pipi@pupu.com'
        self.browser.get(self.live_server_url)
        self.esperar_salida(email)

        self.crear_sesion_preautenticada(email)
        self.browser.get(self.live_server_url)
        self.esperar_ingreso(email)