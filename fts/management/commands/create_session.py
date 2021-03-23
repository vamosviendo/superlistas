from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth import \
    BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore

User = get_user_model()


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('email')

    def handle(self, *args, **options):
        session_key = crear_sesion_preautenticada(options['email'])
        self.stdout.write(session_key)


def crear_sesion_preautenticada(email):
    usuario = User.objects.create(email=email)
    sesion = SessionStore()
    sesion[SESSION_KEY] = usuario.pk
    sesion[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
    sesion.save()
    return sesion.session_key