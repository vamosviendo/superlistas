from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render
from django.views.generic import CreateView, DetailView, FormView

from listas.forms import ItemForm, ItemListaExistenteForm, NuevaListaForm
from listas.models import Lista

User = get_user_model()


def home_page(request):
    return render(request, 'home.html', {'form': ItemForm()})


class HomePageView(FormView):
    template_name = 'home.html'
    form_class = ItemForm


def nueva_lista(request):
    form = NuevaListaForm(data=request.POST)
    if form.is_valid():
        lista = form.save(duenio=request.user)
        return redirect(lista)

    return render(request, 'home.html', {'form': form})


class NuevaListaView(CreateView, HomePageView):
    form_class = NuevaListaForm

    def form_valid(self, form):
        lista = form.save(duenio=self.request.user)
        return redirect(lista)

def view_lista(request, lista_id):
    lista = Lista.objects.get(id=lista_id)
    form = ItemListaExistenteForm(en_lista=lista)

    if request.method == 'POST':
        form = ItemListaExistenteForm(en_lista=lista, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(lista)
    return render(request, 'lista.html', {'lista': lista, 'form': form})


class VerYAgregarALista(DetailView, CreateView):
    model = Lista
    template_name = 'lista.html'
    form_class = ItemListaExistenteForm

    def get_form(self):
        self.object = self.get_object()
        return self.form_class(en_lista=self.object, data=self.request.POST)


def compartir_lista(request, lista_id):
    lista = Lista.objects.get(id=lista_id)
    user = User.objects.get(email=request.POST.get('sharee'))
    lista.compartir_con(user)
    return redirect(lista)


def mis_listas(request, email):
    duenio = User.objects.get(email=email)
    return render(request, 'mis_listas.html', {'duenio': duenio})
