# Django modules
from django.contrib import admin

# Project modules
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """Admin configuration for CustomUser model."""

    list_display = ("email", "first_name", "last_name", "is_active", "is_staff")
    list_filter = ("is_active", "is_staff", "is_superuser")
    search_fields = ("email", "first_name", "last_name")
    readonly_fields = ("created_at", "updated_at", "last_login")
    exclude = ("password",)
