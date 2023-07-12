from django.urls import path
from .views import index, GameListView, GameCategoryListView, GameDetail, search

app_name = "catalog"

urlpatterns = [
    path("", index, name="index"),
    path("catalog/", GameListView.as_view(), name="catalog"),
    path(
        "catalog/<slug:cat_slug>/", GameCategoryListView.as_view(), name="category_list"
    ),
    path("catalog/games/<slug:slug>/", GameDetail.as_view(), name="product_detail"),
    path("search/", search, name="search"),
]
