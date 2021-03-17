from django.shortcuts import redirect, render

from listas.models import Item, Lista


def home_page(request):
    return render(request, 'home.html')


def nueva_lista(request):
    lista = Lista.objects.create()
    Item.objects.create(texto=request.POST['texto_item'], lista=lista)
    return redirect(f'/listas/{lista.id}/')


def agregar_item(request, lista_id):
    lista = Lista.objects.get(id=lista_id)
    Item.objects.create(texto=request.POST['texto_item'], lista=lista)
    return redirect(f'/listas/{lista.id}/')


def view_lista(request, lista_id):
    lista = Lista.objects.get(id=lista_id)
    return render(request, 'lista.html', {'lista': lista})
