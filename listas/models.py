from django.db import models


class Lista(models.Model):
    pass


class Item(models.Model):
    texto = models.TextField(default='')
    lista = models.ForeignKey(Lista, default=None, on_delete=models.CASCADE)
