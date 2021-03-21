from django.test import TestCase

from listas.forms import ItemForm
from listas.models import Item, Lista


class HomePageTest(TestCase):

    def test_home_page_devuelve_html_correcto(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_usa_form_item(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)


class ListaViewTest(TestCase):

    def test_usa_template_lista(self):
        lista = Lista.objects.create()
        response = self.client.get(f'/listas/{lista.id}/')
        self.assertTemplateUsed(response, 'lista.html')

    def test_muestra_solamente_los_items_de_la_lista(self):
        lista_correcta = Lista.objects.create()
        Item.objects.create(texto='Itemio 1', lista=lista_correcta)
        Item.objects.create(texto='Itemio 2', lista=lista_correcta)
        otra_lista = Lista.objects.create()
        Item.objects.create(texto='Item de otra lista 1', lista=otra_lista)
        Item.objects.create(texto='Item de otra lista 2', lista=otra_lista)

        response = self.client.get(f'/listas/{lista_correcta.id}/')

        self.assertContains(response, 'Itemio 1')
        self.assertContains(response, 'Itemio 2')
        self.assertNotContains(response, 'Item de otra lista 1')
        self.assertNotContains(response, 'Item de otra lista 2')

    def test_pasa_la_lista_correcta_al_template(self):
        otra_lista = Lista.objects.create()
        lista_correcta = Lista.objects.create()
        response = self.client.get(f'/listas/{lista_correcta.id}/')
        self.assertEqual(response.context['lista'], lista_correcta)

    def test_puede_guardar_un_request_POST_en_una_lista_existente(self):
        otra_lista = Lista.objects.create()
        lista_correcta = Lista.objects.create()

        self.client.post(
            f'/listas/{lista_correcta.id}/',
            data={'texto_item': 'Nuevo item para lista existente.'}
        )

        self.assertEqual(Item.objects.count(), 1)
        nuevo_item = Item.objects.first()
        self.assertEqual(nuevo_item.texto, 'Nuevo item para lista existente.')
        self.assertEqual(nuevo_item.lista, lista_correcta)

    def test_POST_redirige_a_view_lista(self):
        otra_lista = Lista.objects.create()
        lista_correcta = Lista.objects.create()

        response = self.client.post(
            f'/listas/{lista_correcta.id}/',
            data={'texto_item': 'Nuevo item para lista existente.'}
        )

        self.assertRedirects(response, f'/listas/{lista_correcta.id}/')

    def test_errores_de_validacion_llevan_a_pagina_listas(self):
        lista = Lista.objects.create()
        response = self.client.post(
            f'/listas/{lista.id}/',
            data={'texto_item': ''}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lista.html')
        error_esperado = 'No puede haber un item vacío en la lista.'
        self.assertContains(response, error_esperado)


class NuevaListaViewTest(TestCase):

    def test_puede_guardar_un_request_POST(self):
        self.client.post('/listas/nueva', data={'texto_item': 'Nuevo item'})

        self.assertEqual(Item.objects.count(), 1)
        nuevo_item = Item.objects.first()
        self.assertEqual(nuevo_item.texto, 'Nuevo item')

    def test_redirige_luego_de_un_post(self):
        response = self.client.post(
            '/listas/nueva', data={'texto_item': 'Nuevo item'})
        nueva_lista = Lista.objects.first()
        self.assertRedirects(response, f'/listas/{nueva_lista.id}/')

    def test_errores_de_validacion_se_envian_de_vuelta_a_template_home(self):
        response = self.client.post('/listas/nueva', data={'texto_item': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        error_esperado = 'No puede haber un item vacío en la lista.'
        self.assertContains(response, error_esperado)

    def test_items_de_lista_no_validos_no_se_guardan(self):
        self.client.post('/listas/nueva', data={'texto_item': ''})
        self.assertEqual(Lista.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)
