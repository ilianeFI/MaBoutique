from django.db import models
from django.urls import reverse
# Create your models here.
class Product(models.Model):
    name=models.CharField(max_length=50)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    quantity=models.IntegerField()
    image=models.ImageField(upload_to="products/",blank=True,null=True)
    description=models.TextField(blank=True,null=True)

    def get_absolute_url(self):
        return reverse('product_detail',kwargs={'pk': self.pk})



