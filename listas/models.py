from django.db import models
from django.urls import reverse


class Lista(models.Model):

    def get_absolute_url(self):
        return reverse('view_lista', args=[self.pk])


class Item(models.Model):
    texto = models.TextField(default='')
    lista = models.ForeignKey(Lista, default=None, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('lista', 'texto')
        ordering = ('id', )

    def __str__(self):
        return self.texto
