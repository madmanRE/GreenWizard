from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Post
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from taggit.models import Tag
from profile_app.models import Profile
from .forms import PostCreateForm


class PostListView(ListView):
    template_name = 'blog/list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = (
            Post.objects.filter(availability=True)
        )
        return queryset


class PostDetailView(DetailView):
    template_name = 'blog/detail.html'
    model = Post
    context_object_name = 'post'


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

    context = {
        "posts": posts,
        "author": profile
    }

    return render(request, "blog/list.html", context)


class PostCreateView(LoginRequiredMixin, CreateView):
    template_name = 'blog/create.html'
    form_class = PostCreateForm
    success_url = '/'


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'blog/create.html'
    form_class = PostCreateForm
    success_url = '/'



class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog:blog_list')
