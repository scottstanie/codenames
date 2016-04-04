import datetime
from django.db import models


class Card(models.Model):
    word = models.CharField(max_length=200)
    color = models.CharField(max_length=32)
    chosen = models.BooleanField(default=False)

    def __unicode__(self):
        return '%s: %s' % (self.name, self.id)
