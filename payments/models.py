from django.db import models
from users.models import CustomUser
from orders.models import Order
# Create your models here.
class facture(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    order=models.OneToOneField(Order,on_delete=models.CASCADE)
    date=models.DateField(auto_now_add=True)
    pdf_file = models.FileField(upload_to='factures/', blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10,decimal_places=2)
    is_paid = models.BooleanField(default=False)
