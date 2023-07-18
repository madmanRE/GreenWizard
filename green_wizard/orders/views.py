from django.shortcuts import render, redirect
from .models import OrderItem, Order
from profile_app.models import Profile
from .forms import OrderCreateForm
from cart.cart import Cart
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated and hasattr(request.user, 'profile') and request.user.profile.id:
                order.owner = request.user.profile
                order.save()
                for item in cart:
                    OrderItem.objects.create(order=order,
                                             product=item['product'],
                                             price=item['price'],
                                             quantity=item['quantity'])
                cart.clear()
                send_mail(
                    f"Ваш заказ создан!",
                    f"Номер заказа: {order.id}. Ожидаем оплаты",
                    settings.EMAIL_HOST_USER,
                    [order.email],
                    html_message=f"<p>Уважаемый пользователь, ваш заказ создан.</p>"
                                 f"<p>Обратите внимание на наши другие <a href='http://127.0.0.1:8000/catalog/'>товары</a></p>"
                )
                request.session['order_id'] = order.id
                return redirect(reverse('payment:process'))
            else:
                return HttpResponse("Ошибка: Пользователь не авторизован или профиль пользователя не найден.")
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})


def view_orders(request):
    orders = Order.objects.filter(owner=request.user.profile)
    return render(request, 'orders/list.html', {'orders': orders})



