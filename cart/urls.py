from django.urls import path
from . import views

urlpatterns = [
    path('add/<int:pk>/',views.add_cart,name='add_to_cart'),
    path('cart/',views.showCart,name='cart-detail'),


]