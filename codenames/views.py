from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView

from itertools import chain
import json
import random

from .models import Card, Game, Word, Clue


def index(request):
    with open('./codenames/data.json', 'rb') as word_file:
        colors = ['red', 'blue']
        full_words = json.load(word_file)
        random.shuffle(full_words)
        word_idx = [{'id': idx, 'text': word, 'color': random.choice(colors)} for idx, word in enumerate(full_words[:25])]
        word_rows = [word_idx[i:i + 5] for i in range(0, 25, 5)]

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
        print self.object
        cards = generate_board()
        self.object.cards.add(*cards)
        print self.object.cards
        return reverse('game', kwargs={'unique_id': self.object.unique_id})


def game(request, unique_id):
    return render(request, 'codenames/index.html')


def generate_colors():
    '''Makes a random set of colors legal for a board
    Counts must be (9, 8, 7, 1) of (red/blue, blue/red, grey, black)
    '''
    color_choices = ('red', 'blue', 'grey', 'black')
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


def generate_board():
    words = list(Word.objects.order_by('?')[:25])
    colors = generate_colors()
    cards = [Card(word=w, color=colors[idx]) for idx, w in enumerate(words)]
    for c in cards:
        c.save()
    return cards

def vote(request):
    try:
        winner = get_object_or_404(Item, pk=request.POST['winner'])
        loser = get_object_or_404(Item, pk=request.POST['loser'])
        choice = Choice(winner=winner, loser=loser)
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'codenames/index.html', {
            'error_message': "You didn't select a choice.",
        })
    else:
        winner.votes += 1
        winner.save()
        choice.save()
        # Always return an HttpResponseRedirect after successfully dealing with POST data. This prevents data from being posted twice if a user hits the back button
        print 'winner: ', winner_id
        return HttpResponseRedirect(reverse('codenames:index', kwargs={'winner_id': winner.id}))


@login_required
def profile(request):
    u = request.user
    top_waffles = Item.objects.filter(created_by_id=u.id).order_by('-added_date')
    context = {
        'waffles': top_waffles
    }
    return render(request, 'codenames/profile.html', context)
