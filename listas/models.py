from django.db import models


class Item(models.Model):
    texto = models.TextField(default='')