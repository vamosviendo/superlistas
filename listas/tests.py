from django.test import TestCase

from listas.models import Item, Lista


class HomePageTest(TestCase):

    def test_home_page_devuelve_html_correcto(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class ListaViewTest(TestCase):

    def test_usa_template_lista(self):
        response = self.client.get('/listas/la_unica_lista/')
        self.assertTemplateUsed(response, 'lista.html')

    def test_muestra_todos_los_items(self):
        lista = Lista.objects.create()
        Item.objects.create(texto='Itemio 1', lista=lista)
        Item.objects.create(texto='Itemio 2', lista=lista)

        response = self.client.get('/listas/la_unica_lista/')

        self.assertContains(response, 'Itemio 1')
        self.assertContains(response, 'Itemio 2')


class NuevaListaViewTest(TestCase):

    def test_puede_salvar_un_request_POST(self):
        self.client.post('/listas/nueva', data={'texto_item': 'Nuevo item'})

        self.assertEqual(Item.objects.count(), 1)
        nuevo_item = Item.objects.first()
        self.assertEqual(nuevo_item.texto, 'Nuevo item')

    def test_redirige_luego_de_un_post(self):
        response = self.client.post(
            '/listas/nueva', data={'texto_item': 'Nuevo item'})
        self.assertRedirects(response, '/listas/la_unica_lista/')


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
