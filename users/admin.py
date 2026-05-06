from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser
from unfold.admin import ModelAdmin

@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin, ModelAdmin):
    ordering = ["email"] # On trie par email au lieu de username
    list_display = ["email", "is_staff", "is_superuser"]
    
    # On doit aussi redéfinir fieldsets car l'UserAdmin de base cherche 'username'
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password"),
        }),
    )