# Django modules
from django.contrib import admin

# Project modules
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """Admin configuration for CustomUser model."""

    list_display = (
        "phone",
        "last_name",
        "first_name",
        "role",
        "company",
        "warehouse",
        "is_active",
    )
    list_filter = ("role", "is_active", "is_staff", "company")
    list_select_related = ("company", "warehouse")
    search_fields = ("phone", "email", "first_name", "last_name", "job_title")
    readonly_fields = ("created_at", "updated_at", "last_login", "created_by")
    exclude = ("password",)
