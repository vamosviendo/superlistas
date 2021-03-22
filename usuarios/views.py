from django.contrib import auth, messages
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse

from usuarios.models import Token


def enviar_email_login(request):
    email = request.POST['email']
    token = Token.objects.create(email=email)
    url = request.build_absolute_uri(
        reverse('login') + '?token=' + str(token.uid)
    )
    cuerpo_del_mensaje = f'Usá este enlace para entrar:\n\n{url}'
    send_mail(
        'Tu enlace de entrada a Superlistas',
        cuerpo_del_mensaje,
        'noreply@superlistas',
        [email]
    )
    messages.success(
        request,
        "Busque en su email el enlace para entrar."
    )
    return redirect('/')


def login(request):
    user = auth.authenticate(uid=request.GET.get('token'))
    if user:
        auth.login(request, user)
    return redirect('/')
