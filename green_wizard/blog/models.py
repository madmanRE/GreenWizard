from django.db import models
from taggit.managers import TaggableManager
from profile_app.models import Profile


class Post(models.Model):
    title = models.CharField(max_length=250, verbose_name='Название поста')
    text = models.TextField(verbose_name='Текст поста')
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateField(auto_now=True, verbose_name='Дата изменения')
    tags = TaggableManager()
    author = models.ForeignKey(Profile, null=True, on_delete=models.SET_NULL, related_name='posts', verbose_name='Автор')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Запись блога'
        verbose_name_plural = 'Записи блога'
