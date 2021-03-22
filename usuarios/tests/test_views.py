from unittest.mock import patch, call

from django.test import TestCase

from usuarios.models import Token
import usuarios.views


class ViewEnviarEmailLoginTest(TestCase):

    def test_redirige_a_home(self):
        response = self.client.post(
            '/usuarios/enviar_email_login', data={'email': 'pipi@pupu.com'}
        )
        self.assertRedirects(response, '/')

    def test_envia_mail_a_direccion_tomada_de_post_manual_mock(self):
        self.send_mail_called = False

        def falso_send_mail(subject, body, from_email, to_list):
            self.send_mail_called = True
            self.subject = subject
            self.body = body
            self.from_email = from_email
            self.to_list = to_list

        usuarios.views.send_mail = falso_send_mail

        self.client.post(
            '/usuarios/enviar_email_login', data={'email': 'pipi@pupu.com'})

        self.assertTrue(self.send_mail_called)
        self.assertEqual(self.subject, 'Tu enlace de entrada a Superlistas')
        self.assertEqual(self.from_email, 'noreply@superlistas')
        self.assertEqual(self.to_list, ['pipi@pupu.com'])

    @patch('usuarios.views.send_mail')
    def test_envia_mail_a_direccion_tomada_de_post(self, falso_send_mail):
        self.client.post(
            '/usuarios/enviar_email_login', data={'email': 'pipi@pupu.com'})

        self.assertEqual(falso_send_mail.called, True)
        (subject, body, from_email, to_list), kwargs = falso_send_mail.call_args
        self.assertEqual(subject, 'Tu enlace de entrada a Superlistas')
        self.assertEqual(from_email, 'noreply@superlistas')
        self.assertEqual(to_list, ['pipi@pupu.com'])

    def test_crea_token_asociada_con_el_email(self):
        self.client.post(
            '/usuarios/enviar_email_login', data={'email': 'pipi@pupu.com'})
        token = Token.objects.first()
        self.assertEqual(token.email, 'pipi@pupu.com')

    @patch('usuarios.views.send_mail')
    def test_envia_enlace_login_usando_uid_de_token(self, falso_send_mail):
        self.client.post(
            '/usuarios/enviar_email_login', data={'email': 'pipi@pupu.com'})

        token = Token.objects.first()
        url_esperada = f'http://testserver/usuarios/login?token={token.uid}'
        (subject, body, from_email, to_list), kwargs = falso_send_mail.call_args
        self.assertIn(url_esperada, body)

    def test_muestra_mensaje_de_exito(self):
        response = self.client.post(
            '/usuarios/enviar_email_login',
            data={'email': 'pipi@pupu.com'},
            follow=True
        )

        msj = list(response.context['messages'])[0]
        self.assertEqual(
            msj.message,
            "Busque en su email el enlace para entrar."
        )
        self.assertEqual(msj.tags, "success")


@patch('usuarios.views.auth')
class LoginViewTest(TestCase):

    def test_redirige_a_home(self, falso_auth):
        response = self.client.get('/usuarios/login?token=abcd123')
        self.assertRedirects(response, '/')

    def test_llama_a_authenticate_con_uid_tomada_de_request_get(self, falso_auth):
        self.client.get('/usuarios/login?token=abcd123')
        self.assertEqual(
            falso_auth.authenticate.call_args,
            call(uid='abcd123')
        )

    def test_llama_a_auth_login_con_usuario_si_existe(self, falso_auth):
        response = self.client.get('/usuarios/login?token=abcd123')
        self.assertEqual(
            falso_auth.login.call_args,
            call(response.wsgi_request, falso_auth.authenticate.return_value)
        )

    def test_no_loguea_usuario_si_no_esta_autenticado(self, falso_auth):
        falso_auth.authenticate.return_value = None
        self.client.get('/usuarios/login?token=abcd123')
        self.assertEqual(falso_auth.login.called, False)