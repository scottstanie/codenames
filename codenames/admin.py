from django.contrib import admin

from .models import Word, Card, Game, Clue, Guess


class GameAdmin(admin.ModelAdmin):
    readonly_fields = ('started_date', 'unique_id')

admin.site.register(Word)
admin.site.register(Card)
admin.site.register(Game, GameAdmin)
admin.site.register(Clue)
admin.site.register(Guess)
