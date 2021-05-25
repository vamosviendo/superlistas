from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render

from listas.forms import ItemForm, ItemListaExistenteForm, NuevaListaForm
from listas.models import Lista

User = get_user_model()


def home_page(request):
    return render(request, 'home.html', {'form': ItemForm()})


def nueva_lista(request):
    form = NuevaListaForm(data=request.POST)
    if form.is_valid():
        lista = form.save(duenio=request.user)
        return redirect(lista)

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


def compartir_lista(request, lista_id):
    lista = Lista.objects.get(id=lista_id)
    user = User.objects.get(email=request.POST.get('sharee'))
    lista.compartir_con(user)
    return redirect(lista)


def mis_listas(request, email):
    duenio = User.objects.get(email=email)
    return render(request, 'mis_listas.html', {'duenio': duenio})
