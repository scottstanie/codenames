from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView

from collections import Counter
from itertools import chain
import json
import random

from .models import Card, Game, Word, Clue


def index(request):
    context = {}
    return render(request, 'codenames/index.html', context)


def game(request, unique_id):
    try:
        current_game = get_object_or_404(Game, unique_id=unique_id)
    except (KeyError, Game.DoesNotExist):
        return render(request, 'codenames/index.html', {
            'error_message': "This game doesn't exist.",
        })

    cards = current_game.card_set.order_by('pk')
    word_context = [{'id': idx, 'text': card.word.text, 'color': card.color }
                for idx, card in enumerate(cards)]
    word_rows = [word_context[i:i + 5] for i in range(0, 25, 5)]

    context = {
        'word_rows': word_rows
    }
    return render(request, 'codenames/index.html', context)


class GameCreate(CreateView):
    model = Game
    fields = ['red_giver', 'red_guesser', 'blue_giver', 'blue_guesser']

    def form_valid(self, form):
        # TODO: check that request.user is one of the players
        form.instance.created_by = self.request.user
        return super(GameCreate, self).form_valid(form)

    def get_success_url(self):
        cards = generate_board(self.object)
        # self.object.cards.add(*cards)
        return reverse('game', kwargs={'unique_id': self.object.unique_id})


def generate_colors():
    '''Makes a random set of colors legal for a board
    Counts must be (9, 8, 7, 1) of (red/blue, blue/red, grey, black)
    '''
    rb_counts = [9, 8]
    random.shuffle(rb_counts)
    red_count, blue_count = rb_counts
    grey_count, black_count = 7, 1

    counters = {'red': red_count, 'blue': blue_count,
                'grey': grey_count, 'black': black_count}

    colors = []
    while sum(counters.itervalues()) > 0:
        available_colors = {k: v for k, v in counters.iteritems() if v > 0}
        color = random.choice(available_colors.keys())
        counters[color] -= 1
        colors.append(color)

    return colors


def generate_board(game):
    words = list(Word.objects.order_by('?')[:25])
    colors = generate_colors()
    cards = [Card(word=w, color=colors[idx], game=game) for idx, w in enumerate(words)]
    for c in cards:
        c.save()

    colors = Counter(c.color for c in cards)
    first_color = colors.most_common(1)[0][0]
    game.current_turn = '%s_give' % first_color
    game.save()
    return cards


def move(request):
    choice_text = request.POST['text']
    color = request.POST['color']
    unique_id = request.POST['game_id']
    try:
        game = get_object_or_404(Game, unique_id=unique_id)
        word = get_object_or_404(Word, text=choice_text)
        card = get_object_or_404(Card, word=word, color=color, game=game)
    except (KeyError, Card.DoesNotExist):
        return render(request, 'codenames/index.html', {
            'error_message': "You didn't select a choice.",
        })
    else:
        card.chosen = True
        card.save()
        # Always return an HttpResponseRedirect after successfully dealing with POST data. This prevents data from being posted twice if a user hits the back button
        return HttpResponseRedirect(reverse('game', args=(unique_id,)))


@login_required
def profile(request):
    u = request.user
    red_givers = list(Game.objects.filter(red_giver=u).order_by('-started_date'))
    blue_givers = list(Game.objects.filter(blue_giver=u).order_by('-started_date'))
    red_guessers = list(Game.objects.filter(red_guesser=u).order_by('-started_date'))
    blue_guessers = list(Game.objects.filter(blue_guesser=u).order_by('-started_date'))
    giving = red_givers + blue_givers
    guessing = red_guessers + blue_guessers
    context = {
        'games_giving': giving,
        'games_guessing': guessing
    }
    return render(request, 'codenames/profile.html', context)
