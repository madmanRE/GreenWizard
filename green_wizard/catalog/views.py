from django.shortcuts import render, get_object_or_404
from .models import Game, Category
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView


def index(request):
    return render(request, 'catalog/base.html')


class GameListView(ListView):
    template_name = 'catalog/products/list.html'
    context_object_name = 'games'

    def get_queryset(self):
        return Game.objects.filter(availability=True).order_by(['-number_of_views', '-number_of_sales'])
