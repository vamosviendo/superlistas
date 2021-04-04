from django.contrib.auth import get_user_model
from django.test import TestCase

from listas.forms import ItemForm, ERROR_ITEM_VACIO, ERROR_ITEM_DUPLICADO, ItemListaExistenteForm
from listas.models import Item, Lista

User = get_user_model()


class HomePageTest(TestCase):

    def test_home_page_devuelve_html_correcto(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_usa_form_item(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)


class ListaViewTest(TestCase):

    def postear_entrada_vacia(self):
        lista = Lista.objects.create()
        return self.client.post(f'/listas/{lista.id}/', data={'texto': ''})

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
            data={'texto': 'Nuevo item para lista existente.'}
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
            data={'texto': 'Nuevo item para lista existente.'}
        )

        self.assertRedirects(response, f'/listas/{lista_correcta.id}/')

    def test_la_entrada_invalida_no_se_guarda_en_bd(self):
        self.postear_entrada_vacia()
        self.assertEqual(Item.objects.count(), 0)

    def test_si_la_entrada_no_es_valida_se_muestra_template_lista(self):
        response = self.postear_entrada_vacia()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lista.html')

    def test_si_la_entrada_no_es_valida_se_pasa_form_a_template(self):
        response = self.postear_entrada_vacia()
        self.assertIsInstance(response.context['form'], ItemListaExistenteForm)

    def test_si_la_entrada_no_es_valida_se_muestra_error_en_la_pagina(self):
        response = self.postear_entrada_vacia()
        self.assertContains(response, ERROR_ITEM_VACIO)

    def test_errores_de_validacion_de_items_duplicados_se_muestran_en_pagina_listas(self):
        lista1 = Lista.objects.create()
        item1 = Item.objects.create(lista=lista1, texto='textito')
        response = self.client.post(
            f'/listas/{lista1.id}/',
            data={'texto': 'textito'}
        )
        self.assertContains(response, ERROR_ITEM_DUPLICADO)
        self.assertTemplateUsed(response, 'lista.html')
        self.assertEqual(Item.objects.all().count(), 1)

    def test_muestra_form_item(self):
        lista = Lista.objects.create()
        response = self.client.get(f'/listas/{lista.id}/')
        self.assertIsInstance(response.context['form'], ItemListaExistenteForm)
        self.assertContains(response, 'name="texto"')


class NuevaListaViewTest(TestCase):

    def test_puede_guardar_un_request_POST(self):
        self.client.post('/listas/nueva', data={'texto': 'Nuevo item'})

        self.assertEqual(Item.objects.count(), 1)
        nuevo_item = Item.objects.first()
        self.assertEqual(nuevo_item.texto, 'Nuevo item')

    def test_redirige_luego_de_un_post(self):
        response = self.client.post(
            '/listas/nueva', data={'texto': 'Nuevo item'})
        nueva_lista = Lista.objects.first()
        self.assertRedirects(response, f'/listas/{nueva_lista.id}/')

    def test_si_la_entrada_no_es_valida_muestra_template_home(self):
        response = self.client.post('/listas/nueva', data={'texto': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_errores_de_validacion_se_muestran_en_pagina_home(self):
        response = self.client.post('/listas/nueva', data={'texto': ''})
        self.assertContains(response, ERROR_ITEM_VACIO)

    def test_si_la_entrada_no_es_valida_pasa_form_a_template(self):
        response = self.client.post('/listas/nueva', data={'texto': ''})
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_items_de_lista_no_validos_no_se_guardan(self):
        self.client.post('/listas/nueva', data={'texto': ''})
        self.assertEqual(Lista.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)


class MisListasTest(TestCase):

    def test_url_mis_listas_muestra_template_mis_listas(self):
        User.objects.create(email='a@b.com')
        response = self.client.get('/listas/usuarios/a@b.com/')
        self.assertTemplateUsed(response, 'mis_listas.html')

    def test_pasa_duenio_correcto_a_template(self):
        User.objects.create(email='wrong@owner.com')
        usuario_correcto = User.objects.create(email='a@b.com')
        response = self.client.get('/listas/usuarios/a@b.com/')
        self.assertEqual(response.context['duenio'], usuario_correcto)

    def test_duenio_de_lista_se_guarda_si_usuario_esta_autenticado(self):
        user = User.objects.create(email='a@b.com')
        self.client.force_login(user)
        self.client.post('/listas/nueva', data={'texto': 'item nuevo'})
        lista = Lista.objects.first()
        self.assertEqual(lista.duenio, user)
