from django.contrib import admin
from .models import Game, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'image', 'description', 'show_how_many_games_in']
    prepopulated_fields = {'slug': ('title',)}

    def show_how_many_games_in(self, cat):
        return cat.count_games()

    show_how_many_games_in.short_description = 'Кол-во игр в категории'


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'price', 'quantity', 'availability', 'category', ]
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ['title', 'price', 'quantity', 'number_of_views', 'category']
    search_fields = ['title', 'description']
