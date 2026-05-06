from django.contrib import admin
from .models import Cart, CartItem
from unfold.admin import ModelAdmin, TabularInline

class CartItemInline(TabularInline):
    model = CartItem
    extra = 0

@admin.register(Cart)
class CartAdmin(ModelAdmin):
    list_display = ["user",]
    inlines = [CartItemInline]

@admin.register(CartItem)
class CartItemAdmin(ModelAdmin):
    list_display = ["cart", "product", "quantity"]