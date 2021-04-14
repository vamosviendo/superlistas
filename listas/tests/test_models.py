from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from listas.models import Item, Lista

User = get_user_model()


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

    def test_crear_crea_lista_y_primer_item(self):
        Lista.crear(texto_primer_item='texto de item nuevo')
        item_nuevo = Item.objects.first()
        self.assertEqual(item_nuevo.texto, 'texto de item nuevo')
        lista_nueva = Lista.objects.first()
        self.assertEqual(item_nuevo.lista, lista_nueva)

    def test_crear_devuelve_un_nuevo_objeto_lista(self):
        lista = Lista.crear(texto_primer_item='txt')
        nueva_lista = Lista.objects.first()
        self.assertEqual(lista, nueva_lista)

    def test_listas_pueden_tener_duenios(self):
        Lista(duenio=User())    # No debe dar error

    def test_duenio_es_optativo_en_listas(self):
        Lista().full_clean()    # No debe dar error

    def test_crear_permite_guardar_duenio(self):
        user = User.objects.create()
        Lista.crear(texto_primer_item='texto de item nuevo', duenio=user)
        lista_nueva = Lista.objects.first()
        self.assertEqual(lista_nueva.duenio, user)

    def test_nombre_de_lista_es_el_texto_del_primer_item(self):
        lista = Lista.objects.create()
        Item.objects.create(lista=lista, texto='primer item')
        Item.objects.create(lista=lista, texto='segundo item')
        self.assertEqual(lista.nombre, 'primer item')
