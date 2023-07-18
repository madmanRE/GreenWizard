from django.urls import path
from .views import (
    index,
    GameListView,
    GameCategoryListView,
    GameDetail,
    search,
    products_by_tag,
    product_filter,
)

app_name = "catalog"

urlpatterns = [
    path("", index, name="index"),
    path("catalog/filter/", product_filter, name="product_filter"),
    path("catalog/", GameListView.as_view(), name="catalog"),
    path(
        "catalog/<slug:cat_slug>/", GameCategoryListView.as_view(), name="category_list"
    ),
    path("catalog/tag/<slug:tag_slug>/", products_by_tag, name="products_by_tag"),
    path("catalog/games/<slug:slug>/", GameDetail.as_view(), name="product_detail"),
    path("search/", search, name="search"),
]
