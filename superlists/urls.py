"""superlists URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path

from listas import views as lista_views
from listas import urls as lista_urls
from usuarios import urls as usuarios_urls

urlpatterns = [
    path('', lista_views.HomePageView.as_view(), name='home'),
    path('listas/', include(lista_urls)),
    path('usuarios/', include(usuarios_urls)),
]
