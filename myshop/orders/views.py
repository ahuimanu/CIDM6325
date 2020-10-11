from django.shortcuts import render

from .models import OrderItem
from .forms import OrderCreateForm
from .tasks import order_created
from cart.cart import Cart


# Create your views here.
def order_create(request):
    cart = Cart(request)

    # if it is a POST, process the form
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                        product=item['product'],
                                        price=item['price'],
                                        quantity=item['quantity'])
            # clear the cart
            cart.clear()
            # launch asynchronous task
            order_created.delay(order.id)

            return render(request,
                          'orders/order/created.html',
                          {'order': order})

    # otherwise, assume it is a GET
    else:
        form = OrderCreateForm()
    
    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form})


