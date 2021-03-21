from django.core.exceptions import ValidationError
from django.test import TestCase

from listas.models import Item, Lista


class ListaAndItemModelTest(TestCase):

    def test_salvar_y_recuperar_items(self):
        lista = Lista()
        lista.save()
        primer_item = Item()
        primer_item.texto = 'El primer item de la lista'
        primer_item.lista = lista
        primer_item.save()

        segundo_item = Item()
        segundo_item.texto = 'Segundo item'
        segundo_item.lista = lista
        segundo_item.save()

        lista_guardada = Lista.objects.first()
        self.assertEqual(lista_guardada, lista)

        items_guardados = Item.objects.all()
        self.assertEqual(items_guardados.count(), 2)

        primer_item_guardado = items_guardados[0]
        segundo_item_guardado = items_guardados[1]
        self.assertEqual(
            primer_item_guardado.texto, 'El primer item de la lista')
        self.assertEqual(primer_item_guardado.lista, lista)
        self.assertEqual(segundo_item_guardado.texto, 'Segundo item')
        self.assertEqual(segundo_item_guardado.lista, lista)

    def test_no_puede_guardar_items_de_lista_vacios(self):
        lista = Lista.objects.create()
        item = Item(lista=lista, texto='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_get_absolute_url(self):
        lista = Lista.objects.create()
        self.assertEqual(lista.get_absolute_url(), f'/listas/{lista.id}/')
