from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render

from listas.models import Item, Lista


def home_page(request):
    return render(request, 'home.html')


def nueva_lista(request):
    lista = Lista.objects.create()
    item = Item(texto=request.POST['texto_item'], lista=lista)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        lista.delete()
        error = 'No puede haber un item vacío en la lista.'
        return render(request, 'home.html', {'error': error})
    return redirect(f'/listas/{lista.id}/')


def view_lista(request, lista_id):
    lista = Lista.objects.get(id=lista_id)
    if request.method == 'POST':
        Item.objects.create(texto=request.POST['texto_item'], lista=lista)
        return redirect(f'/listas/{lista.id}/')
    return render(request, 'lista.html', {'lista': lista})
