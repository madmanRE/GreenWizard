from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="профиль")
    username = models.CharField(max_length=100, default="-------")
    password = models.CharField(max_length=20, default="1111")
    phone = models.CharField(
        max_length=20, blank=True, null=True, verbose_name="телефон"
    )
    email = models.EmailField(unique=True, verbose_name="электронная почта")
    avatar = models.ImageField(
        upload_to="profiles/profile",
        null=True,
        default="profiles/profile/ava-default.png",
    )
    discount = models.PositiveIntegerField(
        default=0, verbose_name="накопительная скидка"
    )
    amount_of_purchases = models.PositiveIntegerField(
        default=0, verbose_name="общая сумма покупок"
    )

    def __str__(self):
        return self.username

    def increase_discount(self):
        x = int(self.amount_of_purchases)
        if 10000 < x < 20000:
            self.discount = 5
        elif 20000 < x < 30000:
            self.discount = 12
        elif 30000 < x < 50000:
            self.discount = 20
        elif x > 50000:
            self.discount = 35
        return self.discount

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
