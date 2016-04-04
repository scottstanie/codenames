from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView

from itertools import chain
import json
import random

from .models import Card


def index(request):
    with open('./codenames/data.json', 'rb') as word_file:
        full_words = json.load(word_file)
        random.shuffle(full_words)
        word_idx = [{'id': idx, 'text': word} for idx, word in enumerate(full_words[:25])]
        word_rows = [word_idx[i:i + 5] for i in range(0, 25, 5)]

    context = {
        'word_rows': word_rows
    }
    return render(request, 'codenames/index.html', context)


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
