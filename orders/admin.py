from django.contrib import admin
from .models import Order
from unfold.admin import ModelAdmin
from unfold.decorators import display

@admin.register(Order)
class OrderAdmin(ModelAdmin):
    # On enlève total_price et created_at qui causent l'erreur
    list_display = ["id", "user", "display_status"] 
    list_filter = ["status"] # On enlève created_at du filtre aussi
    search_fields = ["id"]

    @display(description="État", label={
        "pending": "info",
        "completed": "success",
        "cancelled": "danger",
    })
    def display_status(self, obj):
        return obj.status.upper()