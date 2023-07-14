# Generated by Django 4.2.3 on 2023-07-14 09:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0003_post_availability"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="main_img",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="blog/posts/",
                verbose_name="Главное изображение",
            ),
        ),
    ]
