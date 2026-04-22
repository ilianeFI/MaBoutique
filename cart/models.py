from django.db import models
from products.models import Product
from users.models import CustomUser
from django.urls import reverse
# Create your models here.

class Cart(models.Model):
    craeted_at=models.DateTimeField(auto_now_add=True)
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE,null=True)

class CartItem(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    unit_price=models.DecimalField(max_digits=10, decimal_places=2)


