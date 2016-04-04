from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView

from itertools import chain
from .image_finder import Image_finder

from .models import Item, Choice


class ItemCreate(CreateView):
    model = Item
    fields = ['name', 'image_url']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super(ItemCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('polls:profile')


def index(request, winner_id=None):
    waffles = list(Item.objects.exclude(pk=winner_id).order_by('?')[:2])
    if winner_id:
        winner = Item.objects.filter(pk=winner_id)
        waffles = list(chain(winner, waffles))
    context = {
        'waffles': waffles
    }
    return render(request, 'polls/index.html', context)


def vote(request):
    try:
        winner = get_object_or_404(Item, pk=request.POST['winner'])
        loser = get_object_or_404(Item, pk=request.POST['loser'])
        choice = Choice(winner=winner, loser=loser)
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/index.html', {
            'error_message': "You didn't select a choice.",
        })
    else:
        winner.votes += 1
        winner.save()
        choice.save()
        # Always return an HttpResponseRedirect after successfully dealing with POST data. This prevents data from being posted twice if a user hits the back button
        print 'winner: ', winner_id
        return HttpResponseRedirect(reverse('polls:index', kwargs={'winner_id': winner.id}))


def top(request):
    top_waffles = Item.objects.order_by('-votes')[:10]
    context = {
        'waffles': top_waffles
    }
    return render(request, 'polls/top.html', context)


def profile(request):
    u = request.user
    top_waffles = Item.objects.filter(created_by_id=u.id).order_by('-added_date')
    context = {
        'waffles': top_waffles
    }
    return render(request, 'polls/profile.html', context)


def imgsearch(request, keyword="waffles"):
    im = Image_finder()
    img_urls = im.find_photo_urls(num_results=3, text=keyword)
    print keyword
    print img_urls
    return JsonResponse({'imgUrls': img_urls})


@login_required
def add_item(request):
    try:
        print request.POST
        new_item = request.POST
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/index.html', {
            'error_message': "You didn't select a choice.",
        })
    else:
        new_item.save()
        # Always return an HttpResponseRedirect after successfully dealing with POST data. This prevents data from being posted twice if a user hits the back button
        return HttpResponseRedirect(reverse('polls:index'))
