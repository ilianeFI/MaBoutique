from django.shortcuts import render
from django.views import View
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView,CreateView,UpdateView,DeleteView
from .models import Product
# Create your views here.

class Product_list(View):
    def get(self,request):
        products=Product.objects.all()
        return render(request,"product/product.html",{"products":products})


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product/detail.html'
    context_object_name = 'product'

