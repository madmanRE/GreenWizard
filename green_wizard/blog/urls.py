from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    posts_by_tag,
    post_by_author,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
)

app_name = "blog"

urlpatterns = [
    path("update/<slug>/", PostUpdateView.as_view(), name="update_post"),
    path("delete/<slug>/", PostDeleteView.as_view(), name="delete_post"),
    path("create/", PostCreateView.as_view(), name="create_post"),
    path("post/<slug:slug>/", PostDetailView.as_view(), name="blog_detail"),
    path("tag/<slug:tag_slug>/", posts_by_tag, name="posts_by_tag"),
    path("tag/user/<int:user_id>/", post_by_author, name="posts_by_author"),
    path("list/", PostListView.as_view(), name="blog_list"),
]
