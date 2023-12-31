from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager
from profile_app.models import Profile
from django.utils.text import slugify


class Post(models.Model):
    title = models.CharField(max_length=250, verbose_name="Название поста")
    slug = models.SlugField(unique=True, verbose_name="Символьный код")
    main_img = models.ImageField(
        upload_to="blog/posts/",
        blank=True,
        null=True,
        verbose_name="Главное изображение",
    )
    p1 = models.TextField(blank=True, null=True, verbose_name="Параграф 1")
    img1 = models.ImageField(
        upload_to="blog/posts/", blank=True, null=True, verbose_name="Изображение 1"
    )
    p2 = models.TextField(blank=True, null=True, verbose_name="Параграф 2")
    img2 = models.ImageField(
        upload_to="blog/posts/", blank=True, null=True, verbose_name="Изображение 2"
    )
    p3 = models.TextField(blank=True, null=True, verbose_name="Параграф 3")
    img3 = models.ImageField(
        upload_to="blog/posts/", blank=True, null=True, verbose_name="Изображение 3"
    )
    other_text = models.TextField(blank=True, null=True, verbose_name="Остальной текст")
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateField(auto_now=True, verbose_name="Дата изменения")
    tags = TaggableManager()
    author = models.ForeignKey(
        Profile,
        null=True,
        on_delete=models.SET_NULL,
        related_name="posts",
        verbose_name="Автор",
    )
    availability = models.BooleanField(default=True, verbose_name="Доступность")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "blog:blog_detail",
            args=[self.slug],
        )

    class Meta:
        verbose_name = "Запись блога"
        verbose_name_plural = "Записи блога"


class Review(models.Model):
    text = models.TextField(verbose_name="Текст отзыва")
    author = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Владелец отзыва",
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Запись блога",
    )
    created_at = models.DateField(auto_now_add=True, verbose_name="Время публикации")

    def __str__(self):
        return f"Отзыв {self.pk}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
