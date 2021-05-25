from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


User = get_user_model()


class Lista(models.Model):

    duenio = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True, null=True, on_delete=models.CASCADE
    )
    compartida_con = models.ManyToManyField(
        to=User, related_name='listas_compartidas')

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

    def compartir_con(self, usuario):
        self.compartida_con.add(usuario)


class Item(models.Model):
    texto = models.TextField(default='')
    lista = models.ForeignKey(Lista, default=None, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('lista', 'texto')
        ordering = ('id', )

    def __str__(self):
        return self.texto
