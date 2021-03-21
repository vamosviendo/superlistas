from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render

from listas.forms import ItemForm
from listas.models import Item, Lista


def home_page(request):
    return render(request, 'home.html', {'form': ItemForm()})


def nueva_lista(request):
    lista = Lista.objects.create()
    item = Item(texto=request.POST['texto'], lista=lista)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        lista.delete()
        error = 'No puede haber un item vacío en la lista.'
        return render(request, 'home.html', {'error': error})
    return redirect(lista)


def view_lista(request, lista_id):
    lista = Lista.objects.get(id=lista_id)
    error = None

    if request.method == 'POST':
        try:
            item = Item(texto=request.POST['texto'], lista=lista)
            item.full_clean()
            item.save()
            return redirect(lista)
        except ValidationError:
            error = 'No puede haber un item vacío en la lista.'

    return render(request, 'lista.html', {'lista': lista, 'error': error})
