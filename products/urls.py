from django.urls import path
from .views import Product_list,ProductDetailView
urlpatterns = [
    path('product/',Product_list.as_view(),name='product_list' ),
    path('product/<int:pk>/',ProductDetailView.as_view(),name='product_detail'),


]