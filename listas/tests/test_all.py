from django.test import TestCase

from listas.models import Item, Lista


class HomePageTest(TestCase):

    def test_home_page_devuelve_html_correcto(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


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


class NuevaListaViewTest(TestCase):

    def test_puede_guardar_un_request_POST(self):
        self.client.post('/listas/nueva', data={'texto_item': 'Nuevo item'})

        self.assertEqual(Item.objects.count(), 1)
        nuevo_item = Item.objects.first()
        self.assertEqual(nuevo_item.texto, 'Nuevo item')

    def test_puede_guardar_un_request_POST_en_una_lista_existente(self):
        otra_lista = Lista.objects.create()
        lista_correcta = Lista.objects.create()

        self.client.post(
            f'/listas/{lista_correcta.id}/agregar_item',
            data={'texto_item': 'Nuevo item para lista existente.'}
        )

        self.assertEqual(Item.objects.count(), 1)
        nuevo_item = Item.objects.first()
        self.assertEqual(nuevo_item.texto, 'Nuevo item para lista existente.')
        self.assertEqual(nuevo_item.lista, lista_correcta)

    def test_redirige_a_view_lista(self):
        otra_lista = Lista.objects.create()
        lista_correcta = Lista.objects.create()

        response = self.client.post(
            f'/listas/{lista_correcta.id}/agregar_item',
            data={'texto_item': 'Nuevo item para lista existente.'}
        )

        self.assertRedirects(response, f'/listas/{lista_correcta.id}/')

    def test_redirige_luego_de_un_post(self):
        response = self.client.post(
            '/listas/nueva', data={'texto_item': 'Nuevo item'})
        nueva_lista = Lista.objects.first()
        self.assertRedirects(response, f'/listas/{nueva_lista.id}/')


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
