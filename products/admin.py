from django.contrib import admin
from .models import Product
from unfold.admin import ModelAdmin
from unfold.decorators import display

@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ["name", "price", "display_stock", "quantity"]
    search_fields = ["name", "description"]
    list_filter = ["price", "quantity"]
    list_editable = ["price", "quantity"]

    @display(description="Statut Stock", label=True)
    def display_stock(self, obj):
        if obj.quantity == 0:
            return "Rupture de stock", "danger"
        if obj.quantity <= 5:
            return "Stock faible", "warning"
        return "En stock", "success"