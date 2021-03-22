from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.test import TestCase

from usuarios.authentication import PasswordlessAuthenticationBackend
from usuarios.models import Token

User = get_user_model()


class AuthenticateTest(TestCase):

    def test_devuelve_none_si_no_encuentra_el_token(self):
        result = PasswordlessAuthenticationBackend().authenticate(
            HttpRequest(),
            'token-inexistente'
        )
        self.assertIsNone(result)

    def test_devuelve_nuevo_usuario_con_email_correcto_si_encuentra_el_token(self):
        email = 'pipi@pupu.com'
        token = Token.objects.create(email=email)
        usuario = PasswordlessAuthenticationBackend().authenticate(
            HttpRequest(), token.uid)
        nuevo_usuario = User.objects.get(email=email)
        self.assertEqual(usuario, nuevo_usuario)

    def test_devuelve_usuario_existente_con_email_correcto_si_encuentra_el_token(self):
        email = 'pipi@pupu.com'
        usuario_existente = User.objects.create(email=email)
        token = Token.objects.create(email=email)
        usuario = PasswordlessAuthenticationBackend().authenticate(
            HttpRequest(), token.uid)
        self.assertEqual(usuario, usuario_existente)


class GetUserTest(TestCase):

    def test_obtiene_usuario_por_email(self):
        User.objects.create(email='otro@ejemplo.com')
        usuario_deseado = User.objects.create(email='pipi@pupu.com')
        usuario_encontrado = PasswordlessAuthenticationBackend().get_user(
            'pipi@pupu.com'
        )
        self.assertEqual(usuario_encontrado, usuario_deseado)

    def test_devuelve_None_si_no_encuentra_usuario_con_ese_email(self):
        self.assertIsNone(
            PasswordlessAuthenticationBackend().get_user(email='pipi@pupu.com')
        )