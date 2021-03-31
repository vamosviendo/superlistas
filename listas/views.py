from django.shortcuts import redirect, render

from listas.forms import ItemForm, ItemListaExistenteForm
from listas.models import Lista


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
    form = ItemListaExistenteForm(en_lista=lista)

    if request.method == 'POST':
        form = ItemListaExistenteForm(en_lista=lista, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(lista)
    return render(request, 'lista.html', {'lista': lista, 'form': form})


def mis_listas(request, email):
    return render(request, 'mis_listas.html')
