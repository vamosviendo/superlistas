from django.core.exceptions import ValidationError
from django.test import TestCase

from listas.models import Item, Lista


class ItemModelTest(TestCase):

    def test_texto_por_defecto(self):
        item = Item()
        self.assertEqual(item.texto, '')

    def test_item_se_relaciona_con_lista(self):
        lista = Lista.objects.create()
        item = Item()
        item.lista = lista
        item.save()
        self.assertIn(item, lista.item_set.all())

    def test_item_string(self):
        item = Item(texto='un texto')
        self.assertEqual(str(item), 'un texto')

    def test_no_puede_guardar_items_de_lista_vacios(self):
        lista = Lista.objects.create()
        item = Item(lista=lista, texto='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_items_duplicados_no_son_validos(self):
        lista = Lista.objects.create()
        Item.objects.create(lista=lista, texto='bla')
        with self.assertRaises(ValidationError):
            item = Item(lista=lista, texto='bla')
            item.full_clean()

    def test_puede_salvar_el_mismo_item_en_distintas_listas(self):
        lista1 = Lista.objects.create()
        lista2 = Lista.objects.create()
        Item.objects.create(lista=lista1, texto='bla')
        item = Item(lista=lista2, texto='bla')
        item.full_clean()   # No debe tirar error

    def test_ordenamiento_de_lista(self):
        lista1 = Lista.objects.create()
        item1 = Item.objects.create(lista=lista1, texto='i1')
        item2 = Item.objects.create(lista=lista1, texto='item2')
        item3 = Item.objects.create(lista=lista1, texto='3')
        self.assertEqual(
            list(Item.objects.all()),
            [item1, item2, item3]
        )


class ListaModelTest(TestCase):

    def test_get_absolute_url(self):
        lista = Lista.objects.create()
        self.assertEqual(lista.get_absolute_url(), f'/listas/{lista.id}/')
