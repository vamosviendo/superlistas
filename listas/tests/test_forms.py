import unittest
from unittest.mock import patch, Mock
from django.test import TestCase

from listas.forms import (ERROR_ITEM_DUPLICADO, ERROR_ITEM_VACIO, ItemForm,
                          ItemListaExistenteForm, NuevaListaForm)
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


class NuevaListaFormTest(unittest.TestCase):

    @patch('listas.forms.Lista.crear')
    def test_save_crea_lista_nueva_a_partir_de_datos_post_si_el_usuario_no_esta_autenticado(
            self, mockList_crear):
        user = Mock(is_authenticated=False)
        form = NuevaListaForm(data={'texto': 'texto de item nuevo'})
        form.is_valid()
        form.save(duenio=user)
        mockList_crear.assert_called_once_with(
            texto_primer_item='texto de item nuevo'
        )

    @patch('listas.forms.Lista.crear')
    def test_save_crea_lista_nueva_con_duenio_si_el_usuario_esta_autenticado(
            self, mockLista_crear):
        user = Mock(is_authenticated=True)
        form = NuevaListaForm(data={'texto': 'texto de item nuevo'})
        form.is_valid()
        form.save(duenio=user)
        mockLista_crear.assert_called_once_with(
            texto_primer_item='texto de item nuevo', duenio=user
        )

    @patch('listas.forms.Lista.crear')
    def test_save_devuelve_un_nuevo_objeto_lista(self, mockLista_crear):
        user = Mock(is_authenticated=True)
        form = NuevaListaForm(data={'texto': 'texto de item nuevo'})
        form.is_valid()
        response = form.save(duenio=user)
        self.assertEqual(response, mockLista_crear.return_value)
