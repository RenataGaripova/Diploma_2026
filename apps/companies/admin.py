# Django modules
from django.contrib import admin

# Project modules
from .models import Company, Warehouse


class WarehouseInline(admin.TabularInline):
    """Inline configuration for Warehouse model."""

    model = Warehouse
    extra = 0
    fields = ("name", "city", "address", "is_active")


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    """Admin configuration for Company model."""

    list_display = ("name", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name",)
    readonly_fields = ("created_at", "updated_at")
    inlines = (WarehouseInline,)


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    """Admin configuration for Warehouse model."""

    list_display = ("name", "city", "company", "is_active")
    list_filter = ("is_active", "company", "city")
    search_fields = ("name", "city", "address", "company__name")
    readonly_fields = ("created_at", "updated_at")
