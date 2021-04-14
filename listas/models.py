from django.conf import settings
from django.db import models
from django.urls import reverse


class Lista(models.Model):

    duenio = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True, null=True, on_delete=models.CASCADE
    )

    def get_absolute_url(self):
        return reverse('view_lista', args=[self.pk])

    @staticmethod
    def crear(texto_primer_item, duenio=None):
        lista = Lista.objects.create(duenio=duenio)
        Item.objects.create(texto=texto_primer_item, lista=lista)
        return lista

    @property
    def nombre(self):
        return self.item_set.first().texto


class Item(models.Model):
    texto = models.TextField(default='')
    lista = models.ForeignKey(Lista, default=None, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('lista', 'texto')
        ordering = ('id', )

    def __str__(self):
        return self.texto
