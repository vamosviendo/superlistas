from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render

from listas.forms import ItemForm
from listas.models import Item, Lista


def home_page(request):
    return render(request, 'home.html', {'form': ItemForm()})


def nueva_lista(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        lista = Lista.objects.create()
        form.save(en_lista=lista)
        return redirect(lista)
    else:
        return render(request, 'home.html', {'form': form})


def view_lista(request, lista_id):
    lista = Lista.objects.get(id=lista_id)
    form = ItemForm()

    if request.method == 'POST':
        form = ItemForm(data=request.POST)
        if form.is_valid():
            form.save(en_lista=lista)
            return redirect(lista)
    return render(request, 'lista.html', {'lista': lista, 'form': form})
