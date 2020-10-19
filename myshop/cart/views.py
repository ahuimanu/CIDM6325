from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from coupons.forms import CouponApplyForm
from shop.models import Product
from . cart import Cart
from . forms import CartAddProductForm


# Create your views here.
@require_POST
def cart_add(request, product_id):
    """
    View to add product to cart
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 override_quantity=cd['override'])
    
    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    """
    View to remove product from cart
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)

    return redirect('cart:cart_detail')


def cart_detail(request):
    """
    Show current cart contents
    """
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
                            'quantity': item['quantity'],
                            'override': True})

    coupon_apply_form = CouponApplyForm()

    return render(request, 
                  'cart/detail.html', 
                  {'cart': cart,
                   'coupon_apply_form': coupon_apply_form})

