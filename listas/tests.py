from django.test import TestCase

from listas.models import Item


class HomePageTest(TestCase):

    def test_home_page_devuelve_html_correcto(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_puede_salvar_un_request_POST(self):
        self.client.post('/', data={'texto_item': 'Nuevo item'})

        self.assertEqual(Item.objects.count(), 1)
        nuevo_item = Item.objects.first()
        self.assertEqual(nuevo_item.texto, 'Nuevo item')

    def test_redirige_luego_de_un_post(self):
        response = self.client.post('/', data={'texto_item': 'Nuevo item'})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/listas/la_unica_lista/')

    def test_solo_guarda_items_cuando_es_necesario(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)


class ListaViewTest(TestCase):

    def test_usa_template_lista(self):
        response = self.client.get('/listas/la_unica_lista/')
        self.assertTemplateUsed(response, 'lista.html')

    def test_muestra_todos_los_items(self):
        Item.objects.create(texto='Itemio 1')
        Item.objects.create(texto='Itemio 2')

        response = self.client.get('/listas/la_unica_lista/')

        self.assertContains(response, 'Itemio 1')
        self.assertContains(response, 'Itemio 2')


class ItemModelTest(TestCase):

    def test_salvar_y_recuperar_items(self):
        primer_item = Item()
        primer_item.texto = 'El primer item de la lista'
        primer_item.save()

        segundo_item = Item()
        segundo_item.texto = 'Segundo item'
        segundo_item.save()

        items_guardados = Item.objects.all()
        self.assertEqual(items_guardados.count(), 2)

        primer_item_guardado = items_guardados[0]
        segundo_item_guardado = items_guardados[1]
        self.assertEqual(
            primer_item_guardado.texto, 'El primer item de la lista')
        self.assertEqual(segundo_item_guardado.texto, 'Segundo item')
