from django.contrib import admin
from .models import Post, Review
from taggit.models import Tag


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "author"]
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["author", "post"]
