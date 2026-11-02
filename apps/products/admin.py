# Django modules
from django.contrib import admin

# Project modules
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin configuration for Category model."""

    list_display = ("name", "company", "is_active")
    list_filter = ("is_active", "company")
    search_fields = ("name", "company__name")
    readonly_fields = ("created_at", "updated_at")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin configuration for Product model."""

    list_display = ("name", "sku", "unit", "category", "company", "is_active")
    list_filter = ("is_active", "unit", "company", "category")
    list_select_related = ("category", "company")
    search_fields = ("name", "sku")
    readonly_fields = ("created_at", "updated_at", "deleted_at", "created_by")
