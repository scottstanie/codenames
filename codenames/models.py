import hashlib
import time
from django.db import models
from django.contrib.auth.models import User
import django.contrib.postgres.fields as pg_fields


def _createHash():
    """This function generate 10 character long hash"""
    hash = hashlib.sha1()
    hash.update(str(time.time()))
    return hash.hexdigest()[:10]


class Word(models.Model):
    text = models.CharField(max_length=200)

    def __unicode__(self):
        return self.text


class Card(models.Model):
    word = models.ForeignKey(Word)
    chosen = models.BooleanField(default=False)
    color = models.CharField(
        max_length=5,
        choices=(('red', 'red'), ('blue', 'blue'), ('grey', 'grey'), ('black', 'black')),
        default='grey'
    )

    def __unicode__(self):
        return '%s: %s' % (str(self.word), self.color)


class Game(models.Model):
    unique_id = models.CharField(max_length=10, default=_createHash, unique=True)
    url = models.URLField()
    red_giver = models.ForeignKey(User, related_name='red_giver', default=1)
    red_guesser = models.ForeignKey(User, related_name='red_guesser', default=1)
    blue_giver = models.ForeignKey(User, related_name='blue_giver', default=1)
    blue_guesser = models.ForeignKey(User, related_name='blue_guesser', default=1)
    started_date = models.DateTimeField('date started', auto_now_add=True)
    cards = models.ManyToManyField(Card)

    def __unicode__(self):
        return self.unique_id


class Clue(models.Model):
    word = models.CharField(max_length=96)
    number = models.IntegerField()
    giver = models.ForeignKey(User, default=1)

    def __unicode__(self):
        return self.word
