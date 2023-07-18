from itertools import chain
from django.contrib.sitemaps import Sitemap
from itertools import chain
from django.contrib.sitemaps import Sitemap
from .models import Game, Category
from blog.models import Post
from taggit.models import Tag
from django.urls import reverse
from django.utils import timezone


class GreenWizardSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        games = Game.objects.filter(availability=True)
        categories = Category.objects.all()
        posts = Post.objects.filter(availability=True)
        tags = Tag.objects.all()
        return list(chain(posts, categories, games, tags))

    def lastmod(self, obj):
        if not isinstance(obj, Tag) and obj.updated_at:
            return obj.updated_at
        return timezone.now().date()

    def location(self, obj):
        if isinstance(obj, Tag):
            return reverse("catalog:products_by_tag", args=[obj.slug])
        return obj.get_absolute_url()
