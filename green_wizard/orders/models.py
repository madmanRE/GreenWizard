from django.db import models
from catalog.models import Game
from profile_app.models import Profile


class Order(models.Model):
    owner = models.ForeignKey(
        Profile, related_name="orders", on_delete=models.CASCADE, verbose_name="Заказы"
    )
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Отчество")
    email = models.EmailField(verbose_name="Электронная почта")
    address = models.CharField(max_length=250, verbose_name="Адрес")
    postal_code = models.CharField(max_length=20, verbose_name="Почтовые индекс")
    city = models.CharField(max_length=100, verbose_name="Город")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")
    paid = models.BooleanField(default=False, verbose_name="Оплачен")

    class Meta:
        ordering = ["-created"]
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        indexes = [
            models.Index(fields=["-created"]),
        ]

    def __str__(self):
        return f"Order {self.id}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name="items", on_delete=models.CASCADE, verbose_name="Заказ"
    )
    product = models.ForeignKey(
        Game,
        related_name="order_items",
        on_delete=models.CASCADE,
        verbose_name="Товары",
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
