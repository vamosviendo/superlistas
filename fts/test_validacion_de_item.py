from unittest import skip

from .base import FunctionalTest


class ValidacionItemsTest(FunctionalTest):

    @skip
    def test_no_se_puede_agregar_items_vacios_a_la_lista(self):
        self.fail('Escribir!')
