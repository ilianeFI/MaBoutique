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
        if cart_item.quantity<cart_item.product.quantity:
            cart_item.quantity+=1
            cart_item.save()
            messages.success(request, f"{product.name} added to cart successfully!")
        else:
            messages.error(request,f"Stock limit Reached")



    #return redirect(request.META.get('HTTP_REFERER')) cette ligne rederige lutilisatuer doù il vien
    return redirect('cart-detail')

def showCart(request):
    cart=get_or_create_cart(request)
    cart_item=CartItem.objects.filter(cart=cart).select_related("product")
    tva=0.2
    total_price=0
    for item in cart_item:
        total_price+=item.quantity*item.unit_price
    price_ht=total_price
    tva_amount=float(total_price)*0.2
    total_price=float(price_ht)+tva_amount




    return render(request,"cart_detail.html",{
        "total_price":total_price,
        "price_ht":price_ht,
        "cart_item":cart_item
    })


def deleteCart(request):
    cart=get_or_create_cart(request)
    CartItem.objects.filter(cart=cart).delete()

    messages.success(request,f"all cart items are deleted successfully !")

    return redirect("cart-detail")


def deleteCartItem(request,pk):
    cart=get_or_create_cart(request)
    cart_item=get_object_or_404(CartItem,id=pk,cart=cart)


    cart_item.delete()
    messages.success(request, f"{cart_item.product.name} has been deleted successfully")

    return redirect("cart-detail")

def updateCartItem(request,pk):
    cart=get_or_create_cart(request)
    cart_item=get_object_or_404(CartItem,id=pk,cart=cart)
    action=request.POST.get("action")

    if action == "increase":
        if cart_item.quantity<cart_item.product.quantity:
            cart_item.quantity+=1
            cart_item.save()
        else:
            messages.error(request,f"Stock limit Reached")
    elif action == "decrease":
        if cart_item.quantity>1:
            cart_item.quantity-=1
            cart_item.save()
        else:
            messages.error(request,f"you cant have 0 quantity for {cart_item.product.name}")


    return redirect("cart-detail")





