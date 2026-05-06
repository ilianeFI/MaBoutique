from tkinter.constants import CASCADE

from django.db import models
from users.models import CustomUser
# Create your models here.
class Order(models.Model):
    number=models.CharField(max_length=20,unique=True,editable=False)
    date=models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    prix=models.DecimalField(max_digits=10, decimal_places=2)
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('confirmed', 'Confirmée'),
        ('delivered', 'Livrée'),
        ('cancelled', 'Annulée'),
    ]
    status= models.CharField(max_length=20,choices=STATUS_CHOICES,default='pending')
    article=models.IntegerField(null=True)
    

