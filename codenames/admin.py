from django.contrib import admin

from .models import Word, Card, Game, Clue


admin.site.register(Word)
admin.site.register(Card)
admin.site.register(Game)
admin.site.register(Clue)
