# Django modules
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import (
    PROTECT,
    SET_NULL,
    BooleanField,
    CharField,
    ForeignKey,
    Q,
    TextChoices,
    UniqueConstraint,
)
from django.utils.translation import gettext_lazy as _

# Project modules
from apps.abstracts.models import AbstractBaseModel, AbstractSoftDeleteModel
from apps.companies.models import Company


class Category(AbstractBaseModel):
    """Category database model."""

    MAX_NAME_LENGTH = 128

    company = ForeignKey(
        Company,
        on_delete=PROTECT,
        related_name="categories",
        verbose_name=_("Company"),
    )
    name = CharField(
        max_length=MAX_NAME_LENGTH,
        verbose_name=_("Name"),
    )
    is_active = BooleanField(
        default=True, verbose_name=_("Is category active?")
    )

    class Meta:
        """Meta options."""

        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ["name"]
        constraints = [
            UniqueConstraint(
                fields=["company", "name"],
                name="uq_category_company_name",
            ),
        ]

    def __str__(self):
        """Returns string representation of an object"""
        return self.name


class Product(AbstractSoftDeleteModel):
    """Product database model."""

    class Unit(TextChoices):
        """Units of measurement."""

        PIECE = "pcs", _("pcs")
        KILOGRAM = "kg", _("kg")
        LITER = "l", _("l")
        METER = "m", _("m")
        PACK = "pack", _("pack")

    MAX_NAME_LENGTH = 255
    MAX_SKU_LENGTH = 64
    MAX_UNIT_LENGTH = 16

    company = ForeignKey(
        Company,
        on_delete=PROTECT,
        related_name="products",
        verbose_name=_("Company"),
    )
    category = ForeignKey(
        Category,
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name="products",
        verbose_name=_("Category"),
    )
    name = CharField(
        max_length=MAX_NAME_LENGTH,
        verbose_name=_("Name"),
    )
    # артикул
    sku = CharField(
        max_length=MAX_SKU_LENGTH,
        verbose_name=_("SKU"),
    )
    unit = CharField(
        max_length=MAX_UNIT_LENGTH,
        choices=Unit.choices,
        default=Unit.PIECE,
        verbose_name=_("Unit"),
    )
    is_active = BooleanField(
        default=True, verbose_name=_("Is product active?")
    )
    created_by = ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name=_("Created by"),
    )

    class Meta:
        """Meta options."""

        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        ordering = ["name"]
        constraints = [
            UniqueConstraint(
                fields=["company", "sku"],
                condition=Q(deleted_at__isnull=True),
                name="uq_product_company_sku",
                violation_error_message=_(
                    "Product with this SKU already exists in the company"
                ),
            ),
        ]

    def __str__(self):
        """Returns string representation of an object"""
        return f"{self.name} ({self.sku})"

    def clean_fields(self, exclude=None) -> None:
        """Strips spaces around SKU."""
        self.sku = (self.sku or "").strip()
        super().clean_fields(exclude=exclude)

    def clean(self) -> None:
        """Validates that category belongs to the same company."""
        super().clean()
        if (
            self.category_id
            and self.company_id
            and self.category.company_id != self.company_id
        ):
            raise ValidationError({
                "category": _("Category belongs to another company")
            })
