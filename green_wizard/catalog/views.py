from django.shortcuts import render, get_object_or_404
from .models import Game, Category
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.postgres.search import TrigramSimilarity
from .forms import SearchForm, FilterForm
from cart.forms import CartAddProductForm
from taggit.models import Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
    return render(
        request,
        "catalog/products/index.html",
        {"cart_product_form": CartAddProductForm()},
    )


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
        sort_param = self.request.GET.get("sort_by", None)
        queryset = Game.objects.filter(availability=True).order_by(
            "-number_of_views", "-number_of_sales"
        )
        if sort_param == "price":
            queryset = Game.objects.filter(availability=True).order_by("-price")
        elif sort_param == "reviews":
            queryset = Game.objects.filter(availability=True).order_by(
                "-number_of_views"
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page"] = self.page
        context["tags"] = Tag.objects.all()[:10]
        context["cart_product_form"] = CartAddProductForm()
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
        sort_param = self.request.GET.get("sort_by", None)
        queryset = (
            Game.objects.filter(availability=True, category=self.category)
            .order_by("-number_of_views", "-number_of_sales")
            .select_related("category")
        )
        if sort_param == "price":
            queryset = (
                Game.objects.filter(availability=True, category=self.category)
                .order_by("-price")
                .select_related("category")
            )
        elif sort_param == "reviews":
            queryset = (
                Game.objects.filter(availability=True, category=self.category)
                .order_by("-number_of_views")
                .select_related("category")
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        context["page"] = self.page
        context["cart_product_form"] = CartAddProductForm()
        return context


class GameDetail(DetailView):
    template_name = "catalog/products/detail.html"
    model = Game
    context_object_name = "game"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        game = self.object
        context["game"] = game
        context["cart_product_form"] = CartAddProductForm()
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
        {
            "form": form,
            "query": query,
            "results": results,
            "cart_product_form": CartAddProductForm(),
        },
    )


def products_by_tag(request, tag_slug):
    tag = Tag.objects.get(slug=tag_slug)

    products = Game.objects.filter(tags=tag)
    sort_param = request.GET.get("sort_by", None)

    if sort_param == "price":
        products = Game.objects.filter(tags=tag).order_by("-price")
    elif sort_param == "reviews":
        products = Game.objects.filter(tags=tag).order_by("-number_of_views")

    paginator = Paginator(products, 16)

    page_num = request.GET.get("page", 1)
    page = paginator.get_page(page_num)

    context = {
        "tag": tag,
        "games": page.object_list,
        "page": page,
        "cart_product_form": CartAddProductForm(),
    }
    return render(request, "catalog/products/list.html", context)


def product_filter(request):
    form = FilterForm(request.GET)
    games = Game.objects.all()

    if form.is_valid():
        min_price = form.cleaned_data["min_price"]
        max_price = form.cleaned_data["max_price"]
        age_limit = form.cleaned_data["age_limit"]
        amount_people = form.cleaned_data["amount_people"]

        if min_price:
            games = games.filter(price__gte=min_price)
        if max_price:
            games = games.filter(price__lte=max_price)
        if age_limit:
            games = games.filter(age_limit__gte=age_limit)
        if amount_people:
            games = games.filter(number_of_persons=amount_people)

    paginator = Paginator(games, 16)

    page_num = request.GET.get("page", 1)
    page = paginator.get_page(page_num)

    context = {
        "games": page.object_list,
        "page": page,
        "form": form,
        "cart_product_form": CartAddProductForm(),
    }
    return render(request, "catalog/products/list.html", context)
