from django.test import TestCase
from django.contrib.auth import get_user_model

from usuarios.models import Token

User = get_user_model()


class UserModelTest(TestCase):

    def test_usuario_es_valido_solo_con_email(self):
        usuario = User(email='a@b.com')
        usuario.full_clean()   # No debe tirar error

    def test_email_como_clave_primaria(self):
        usuario = User(email='a@b.com')
        self.assertEqual(usuario.pk, 'a@b.com')


class TokenModelTest(TestCase):

    def test_enlaza_usuario_con_uid_autogenerada(self):
        token1 = Token.objects.create(email='a@b.com')
        token2 = Token.objects.create(email='a@b.com')
        self.assertNotEqual(token1.uid, token2.uid)
