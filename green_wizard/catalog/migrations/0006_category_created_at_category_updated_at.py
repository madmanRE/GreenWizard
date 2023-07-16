# Generated by Django 4.2.3 on 2023-07-15 11:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0005_game_created_at_game_updated_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="created_at",
            field=models.DateField(
                auto_now_add=True,
                default=datetime.datetime(
                    2023, 7, 15, 11, 1, 57, 582154, tzinfo=datetime.timezone.utc
                ),
                verbose_name="Дата добавления категории",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="category",
            name="updated_at",
            field=models.DateField(
                auto_now=True, verbose_name="Дата последнего изменения"
            ),
        ),
    ]
