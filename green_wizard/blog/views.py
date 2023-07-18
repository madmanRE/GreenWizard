from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.urls import reverse_lazy
from .models import Post
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from taggit.models import Tag
from profile_app.models import Profile
from .forms import PostCreateForm, ReviewForm
from django.http import HttpResponseRedirect, HttpResponse


class PostListView(ListView):
    template_name = "blog/list.html"
    context_object_name = "posts"

    def get_queryset(self):
        queryset = Post.objects.filter(availability=True)
        return queryset


class PostDetailView(DetailView):
    def get(self, request, *args, **kwargs):
        slug = kwargs.get("slug")
        post = get_object_or_404(Post, slug=slug)
        form = ReviewForm(author=request.user)
        context = {
            "post": post,
            "form": form,
            "comments": post.reviews.all(),
        }
        return render(request, "blog/detail.html", context)

    def post(self, request, *args, **kwargs):
        slug = kwargs.get("slug")
        author = None
        try:
            user = request.user.profile
        except:
            pass
        post = get_object_or_404(Post, slug=slug)
        form = ReviewForm(request.POST, author=request.user.profile)
        if form.is_valid():
            form.instance.post = post
            form.save()
            return HttpResponseRedirect(reverse("blog:blog_detail", args=[slug]))


def posts_by_tag(request, tag_slug):
    tag = Tag.objects.get(slug=tag_slug)
    posts = Post.objects.filter(tags=tag)

    context = {
        "tag": tag,
        "posts": posts,
    }
    return render(request, "blog/list.html", context)


def post_by_author(request, user_id):
    profile = Profile.objects.get(id=user_id)
    posts = Post.objects.filter(author=profile)

    context = {"posts": posts, "author": profile}

    return render(request, "blog/list.html", context)


class PostCreateView(LoginRequiredMixin, CreateView):
    template_name = "blog/create.html"
    form_class = PostCreateForm
    success_url = "/"

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.instance.author = self.request.user.profile
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = "blog/create.html"
    form_class = PostCreateForm
    success_url = "/"


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("blog:blog_list")
