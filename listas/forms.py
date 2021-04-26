from django import forms
from django.core.exceptions import ValidationError

from listas.models import Item, Lista

ERROR_ITEM_VACIO = 'No puede haber un item vacío en la lista.'
ERROR_ITEM_DUPLICADO = 'Ya existe ese item en la lista'


class ItemForm(forms.models.ModelForm):

    class Meta:
        model = Item
        fields = ('texto', )
        widgets = {
            'texto': forms.fields.TextInput(attrs={
                'placeholder': 'Ingrese una tarea',
                'class': 'form-control input-lg',
            }),
        }
        error_messages = {
            'texto': {'required': ERROR_ITEM_VACIO}
        }


class NuevaListaForm(ItemForm):

    def save(self, duenio):
        if duenio.is_authenticated:
            return Lista.crear(
                texto_primer_item=self.cleaned_data['texto'], duenio=duenio)
        return Lista.crear(texto_primer_item=self.cleaned_data['texto'])


class ItemListaExistenteForm(ItemForm):

    def __init__(self, en_lista, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.lista = en_lista

    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {'texto': [ERROR_ITEM_DUPLICADO]}
            self._update_errors(e)

    def test_form_save(self):
        lista = Lista.objects.create()
        form = ItemListaExistenteForm(en_lista=lista, data={'texto': 'hola'})
        item_nuevo = form.save()
        self.assertEqual(item_nuevo, Item.objects.all()[0])

    # def save(self):
    #     return forms.models.ModelForm.save(self)
