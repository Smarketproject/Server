from django.db import models


class Weight(models.Model):
    value = models.FloatField('Valor', max_length=128)
    cart = models.ForeignKey('core.Cart')