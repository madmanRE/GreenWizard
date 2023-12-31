# Generated by Django 4.2.3 on 2023-07-14 21:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("profile_app", "0002_profile_password"),
        ("blog", "0004_post_main_img"),
    ]

    operations = [
        migrations.CreateModel(
            name="Review",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.TextField(verbose_name="Текст отзыва")),
                (
                    "created_at",
                    models.DateField(
                        auto_now_add=True, verbose_name="Время публикации"
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reviews",
                        to="profile_app.profile",
                        verbose_name="Владелец отзыва",
                    ),
                ),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reviews",
                        to="blog.post",
                        verbose_name="Запись блога",
                    ),
                ),
            ],
            options={
                "verbose_name": "Отзыв",
                "verbose_name_plural": "Отзывы",
            },
        ),
    ]
