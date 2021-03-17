from django.shortcuts import redirect, render

from listas.models import Item, Lista


def home_page(request):
    return render(request, 'home.html')


def nueva_lista(request):
    lista = Lista.objects.create()
    Item.objects.create(texto=request.POST['texto_item'], lista=lista)
    return redirect('/listas/la_unica_lista/')


def view_lista(request):
    items = Item.objects.all()
    return render(request, 'lista.html', {'items': items})
