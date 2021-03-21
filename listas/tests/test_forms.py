from django.test import TestCase

from listas.forms import (
    ERROR_ITEM_DUPLICADO, ERROR_ITEM_VACIO, ItemForm, ItemListaExistenteForm)
from listas.models import Lista, Item


class ItemFormTest(TestCase):

    def test_form_campo_item_tiene_placeholder_y_clases_css(self):
        form = ItemForm()
        self.assertIn('placeholder="Ingrese una tarea"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validacion_para_items_en_blanco(self):
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['texto'], [ERROR_ITEM_VACIO])

    def test_form_save_maneja_el_guardado_en_una_lista(self):
        lista = Lista.objects.create()
        form = ItemForm(data={'texto': 'hacerme'})
        nuevo_item = form.save(en_lista=lista)
        self.assertEqual(nuevo_item, Item.objects.first())
        self.assertEqual(nuevo_item.texto, 'hacerme')
        self.assertEqual(nuevo_item.lista, lista)


class ItemListaExistenteFormTest(TestCase):

    def test_form_muestra_campo_de_entrada_de_item(self):
        lista = Lista.objects.create()
        form = ItemListaExistenteForm(en_lista=lista)
        self.assertIn('placeholder="Ingrese una tarea"', form.as_p())

    def test_form_chequea_items_en_blanco(self):
        lista = Lista.objects.create()
        form = ItemListaExistenteForm(en_lista=lista, data={'texto': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['texto'], [ERROR_ITEM_VACIO])

    def test_form_chequea_items_duplicados(self):
        lista = Lista.objects.create()
        Item.objects.create(lista=lista, texto='sin duplicados!')
        form = ItemListaExistenteForm(
            en_lista=lista, data={'texto': 'sin duplicados!'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['texto'], [ERROR_ITEM_DUPLICADO])

