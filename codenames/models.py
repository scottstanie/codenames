import hashlib
import time
from django.db import models
from django.contrib.auth.models import User


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
    color = models.ArrayField(models.IntegerField())
    chosen = models.BooleanField(default=False)

    def __unicode__(self):
        return self.word


class Board(models.model):
    game = models.ForeignKey('Game')
    cards = models.ManyToManyField(Card)

    def __unicode__(self):
        return self.game


class Game(models.Model):
    unique_id = models.CharField(max_length=10, default=_createHash, unique=True)
    url = models.URLField()
    red_giver = models.ForeignKey(User, related_name='red_giver', default=1)
    red_guesser = models.ForeignKey(User, related_name='red_guesser', default=1)
    blue_giver = models.ForeignKey(User, related_name='blue_giver', default=1)
    blue_guesser = models.ForeignKey(User, related_name='blue_guesser', default=1)
    started_date = models.DateTimeField('date started', auto_now_add=True)
    board = models.ForeignKey(Board)

    def __unicode__(self):
        return self.url


class Clue(models.Model):
    word = models.CharField(max_length=96)
    number = models.IntegerField()
    giver = models.ForeignKey(User, default=1)

    def __unicode__(self):
        return self.word
