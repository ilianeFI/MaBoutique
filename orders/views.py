from django.shortcuts import render, redirect, get_object_or_404
from cart.models import CartItem
from cart.views import get_or_create_cart,get_total_price
from orders.forms import OrderForm
from .models import Order
import uuid
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.

def create_order(request):
    #cas 1 user est conncete
    if request.user.is_authenticated:
        cart=get_or_create_cart(request)
        if request.method == 'POST':
            form = OrderForm(request.POST)#cette ligne cest pour preparer un formulaire et traduir les donnes
            if form.is_valid():
                order=form.save(commit=False)#cette ligne cest pour creer une instance de Order mais vide
                order.user=request.user
                cart_item=CartItem.objects.filter(cart=cart).select_related('product')
                order.prix=get_total_price(cart_item)
                order.number = str(uuid.uuid4())[:10].upper()
                cart_item=CartItem.objects.filter(cart=cart)
                articles=0
                for item in cart_item:
                    articles+=1
                order.article=articles
                order.save()
                return redirect('order_page', order_number=order.number)
        else:
            form=OrderForm()
            return redirect('home')

    #si l'invite a clicker sur passer Commande
    else:
        return redirect('/register/?next=order')


def order_page(request,order_number):
    order=get_object_or_404(Order,number=order_number,user=request.user)
    cart=get_or_create_cart(request)
    cart_item=CartItem.objects.filter(cart=cart).select_related("product")
    total_price=order.prix
    total_price = float(total_price) +float(total_price)*0.2
    return render(request, "order.html",{
        'cart': cart,
        'order':order,
        'total_price':total_price,
    })


def valider_order(request,order_id):
    order=get_object_or_404(Order,id=order_id,user=request.user)
    if request.method == 'POST':
        order.status='confirmed'
        order.save()
        messages.success(request,"Order Valider avec success")
        return redirect('paiment',order.id)#paiment
    else:
        return redirect('home')

def annuler_order(request,order_id):
    order=get_object_or_404(Order,id=order_id,user=request.user)
    if request.method == 'POST':
        order.status='cancelled'
        order.save()
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect(request.META.get('HTTP_REFERER'))


@login_required
def order_list(request):
    orders=Order.objects.filter(user=request.user).order_by('-date')
    orders_pending=orders.filter(status='pending')
    orders_delivered=orders.filter(status='delivered')
    return render(request,'orders_list.html',{
        'orders':orders,
        'orders_pending':orders_pending,
        'orders_delivered':orders_delivered,
    })
