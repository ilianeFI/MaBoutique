from django.shortcuts import render
import stripe
from django.conf import settings
from django.shortcuts import redirect, get_object_or_404
from orders.models import Order
from django.urls import reverse
from cart.views import get_or_create_cart,deleteCart

# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY


def process_stripe_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # Création de la session Stripe
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'mad',
                'unit_amount': int(order.prix * 100),
                'product_data': {
                    'name': f'Commande #{order.number}',
                },
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(
            reverse('paiment_success', kwargs={'order_id': order.id})
        ),
        cancel_url=request.build_absolute_uri(
            reverse('payment_failed')
        )
    )

    # Redirection vers la page sécurisée de Stripe
    return redirect(session.url, code=303)
def paiment_choix(request,order_id):
    order=get_object_or_404(Order,id=order_id,user=request.user)
    return render(request,'paiment.html',{'order':order})

def paiment_selection(request,order_id):
    order=get_object_or_404(Order,id=order_id,user=request.user)
    if request.method=='POST':
        method = request.POST.get('payment_method')
        if method=='cash':
            return redirect('paiment_success',order_id)
        if method =='card':
            return process_stripe_payment(request,order_id)
    return redirect('paiment',order_id)

def paiment_success(request,order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order.status='delivered'
    order.save()
    deleteCart(request)
    return render(request,'success.html',{'order':order})

def payment_failed(request):

    return render(request,'failed.html',{})