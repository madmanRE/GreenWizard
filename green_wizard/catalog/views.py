from django.shortcuts import render, get_object_or_404
from .models import Game, Category
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.postgres.search import TrigramSimilarity
from .forms import SearchForm
from django.core.paginator import Paginator


def index(request):
    return render(request, "catalog/base.html")


class GameListView(ListView):
    template_name = "catalog/products/list.html"
    context_object_name = "games"
    paginate_by = 16

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        self.paginator = Paginator(self.object_list, self.paginate_by)
        page_number = request.GET.get("page")
        self.page = self.paginator.get_page(page_number)
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_queryset(self):
        queryset = Game.objects.filter(availability=True).order_by(
            "-number_of_views", "-number_of_sales"
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page"] = self.page
        return context


class GameCategoryListView(ListView):
    template_name = "catalog/products/list.html"
    context_object_name = "games"
    paginate_by = 16

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.category = Category.objects.get(slug=self.kwargs["cat_slug"])

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        self.paginator = Paginator(self.object_list, self.paginate_by)
        page_number = request.GET.get("page")
        self.page = self.paginator.get_page(page_number)
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_queryset(self):
        queryset = (
            Game.objects.filter(availability=True, category=self.category)
            .order_by("-number_of_views", "-number_of_sales")
            .select_related("category")
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        context["page"] = self.page
        return context


class GameDetail(DetailView):
    template_name = "catalog/products/detail.html"
    model = Game
    context_object_name = "game"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        game = self.object
        context["game"] = game
        game.do_number_of_views_plus()
        return context


def search(request):
    form = SearchForm()
    query = None
    results = []

    if "query" in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data["query"]
            results = (
                Game.objects.annotate(
                    similarity=TrigramSimilarity("title", query),
                )
                .filter(similarity__gt=0.1)
                .order_by("-similarity")
            )
    return render(
        request,
        "catalog/products/search.html",
        {"form": form, "query": query, "results": results},
    )
