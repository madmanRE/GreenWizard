from .models import Category, Game


def categories(request):
    return {'categories': Category.objects.all()}


def most_popular_games(request):
    return {'most_popular_games': Game.objects.all().order_by('-number_of_views')[:12]}

