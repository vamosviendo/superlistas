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
from django.urls import path

from listas import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('listas/nueva', views.nueva_lista, name='nueva_lista'),
    path('listas/<int:lista_id>/', views.view_lista, name='view_lista'),
    path(
        'listas/<int:lista_id>/agregar_item',
        views.agregar_item,
        name='agregar_item'
    ),
]
