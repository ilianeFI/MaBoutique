from django.urls import path
from . import views

urlpatterns = [
    path('add/<int:pk>/',views.add_cart,name='add_to_cart'),
    path('cart/',views.show_cart,name='cart-detail'),

    path('cart/delete/',views.deleteCart,name='delete_cart'),
    path('cart/delete/<int:pk>/',views.deleteCartItem,name='delete_cartItem'),

    path('cart/update/<int:pk>/',views.updateCartItem,name='update_cartItem'),


]