from django.db import models
from django.db.models import Count
from taggit.managers import TaggableManager
from django.utils.text import slugify


class Game(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    slug = models.SlugField(unique=True, verbose_name="Символьный код")
    image = models.URLField(verbose_name="Адрес изображения")
    price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, verbose_name="Цена"
    )
    number_of_persons = models.CharField(
        max_length=10, verbose_name="Количество игроков"
    )
    duration = models.CharField(max_length=10, verbose_name="Продолжительность")
    age_limit = models.PositiveIntegerField(
        default=12, verbose_name="Ограничение по возрасту"
    )
    quantity = models.PositiveIntegerField(
        default=0, verbose_name="Количество на складе"
    )
    availability = models.BooleanField(default=True, verbose_name="Доступность")
    number_of_views = models.PositiveIntegerField(
        default=0, verbose_name="Кол-во просмотров"
    )
    number_of_sales = models.PositiveIntegerField(
        default=0, verbose_name="Кол-во покупок"
    )
    category = models.ForeignKey(
        "Category",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="games",
        verbose_name="Категория игры",
    )
    tags = TaggableManager()

    # bounded_games = //TODO возможно, стоит задать связанные игры самому, возможно реализовать через Redis
    # image_gallery = //TODO точно стоит задать галерею изображений к конкретному товару, но делать этого не буду, т.к. буду парсить сайт конкурентов, чтобы заполнить БД и брать будут только адрес изображений с превью

    class Meta:
        verbose_name = "Игра"
        verbose_name_plural = "Игры"
        ordering = ["-id"]

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.availability = False
        self.save()

    def hard_delete(self, *args, **kwargs):
        self.delete(*args, **kwargs)

    def get_absolute_url(self):
        pass

    def likely_games(self):
        res = Game.objects.filter(
            number_of_persons=self.number_of_persons, age_limit=self.age_limit
        ).exclude(id=self.id)[:7]
        return res

    def do_number_of_views_plus(self):
        self.number_of_views += 1
        self.save()


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название категорий")
    slug = models.SlugField(unique=True, verbose_name="Символьный код")
    image = models.ImageField(
        upload_to="categories/%Y/cat/", blank=True, verbose_name="Изображение"
    )
    description = models.TextField(verbose_name="Описание")

    class Meta:
        verbose_name = "Категория игр"
        verbose_name_plural = "Категории игр"

    def __str__(self):
        return self.title

    def count_games(self):
        return self.games.count()

    def get_absolute_url(self):
        pass
