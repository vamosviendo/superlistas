from django.conf import settings
from django.contrib.auth import \
    BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore

from fts.base import FunctionalTest

User = get_user_model()


class MisListasTest(FunctionalTest):

    def crear_sesion_preautenticada(self, email):
        usuario = User.objects.create(email=email)
        sesion = SessionStore()
        sesion[SESSION_KEY] = usuario.pk
        sesion[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        sesion.save()
        self.browser.get(self.live_server_url + '/404_no_existe/')
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=sesion.session_key,
            path='/',
        ))

    def test_listas_de_usuario_logueado_se_guardan_como_llmis_listasll(self):
        email = 'pipi@pupu.com'
        self.browser.get(self.live_server_url)
        self.esperar_salida(email)

        self.crear_sesion_preautenticada(email)
        self.browser.get(self.live_server_url)
        self.esperar_ingreso(email)