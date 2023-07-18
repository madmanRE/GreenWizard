from django.shortcuts import render
from .models import OrderItem
from profile_app.models import Profile
from .forms import OrderCreateForm
from cart.cart import Cart
from django.http import HttpResponse



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
                return render(request, 'orders/order/created.html', {'order': order})
            else:
                return HttpResponse("Ошибка: Пользователь не авторизован или профиль пользователя не найден.")
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})







