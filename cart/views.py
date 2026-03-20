from django.http import HttpResponse

from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from .models import Cart,CartItem
from products.models import Product
from django.contrib import messages


# Create your views here.

def get_or_create_cart(request):
    cart_id=request.session.get('cart_id')

    if cart_id:
        try:
            return Cart.objects.get(id=cart_id)
        except Cart.DoesNotExist:
            pass


    cart=Cart.objects.create()
    request.session['cart_id']=cart.id
    return cart


def add_cart(request,pk):
    cart=get_or_create_cart(request)
    product = get_object_or_404(Product, id=pk)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1, 'unit_price': product.price}
    )

    if not created:
        cart_item.quantity+=1
        cart_item.save()

    messages.success(request, f"{product.name} added to cart successfully!")

    return redirect(request.META.get('HTTP_REFERER'))

def showCart(request):
    cart=get_or_create_cart(request)
    cart_item=CartItem.objects.filter(cart=cart).select_related("product")
    total_price=0
    for item in cart_item:
        total_price+=item.quantity*item.unit_price



    return render(request,"cart_detail.html",{"total_price":total_price,"cart_item":cart_item})





