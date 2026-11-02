# Django modules
from django.db.models import (
    PROTECT,
    BooleanField,
    CharField,
    ForeignKey,
    UniqueConstraint,
)
from django.utils.translation import gettext_lazy as _

# Project modules
from apps.abstracts.models import AbstractBaseModel


class Company(AbstractBaseModel):
    """Company database model."""

    MAX_NAME_LENGTH = 128

    name = CharField(
        max_length=MAX_NAME_LENGTH,
        verbose_name=_("Name"),
    )
    is_active = BooleanField(
        default=True, verbose_name=_("Is company active?")
    )

    class Meta:
        """Meta options."""

        verbose_name = _("Company")
        verbose_name_plural = _("Companies")
        ordering = ["-created_at"]

    def __str__(self):
        """Returns string representation of an object"""
        return self.name

    @property
    def has_multiple_warehouses(self) -> bool:
        """Returns True if the company has >1 active warehouse."""
        return self.warehouses.filter(is_active=True).count() > 1


class Warehouse(AbstractBaseModel):
    """Warehouse database model."""

    MAX_NAME_LENGTH = 128
    MAX_CITY_LENGTH = 64
    MAX_ADDRESS_LENGTH = 255

    company = ForeignKey(
        Company,
        on_delete=PROTECT,
        related_name="warehouses",
        verbose_name=_("Company"),
    )
    name = CharField(
        max_length=MAX_NAME_LENGTH,
        verbose_name=_("Name"),
    )
    city = CharField(
        max_length=MAX_CITY_LENGTH,
        verbose_name=_("City"),
    )
    address = CharField(
        max_length=MAX_ADDRESS_LENGTH,
        blank=True,
        verbose_name=_("Address"),
    )
    is_active = BooleanField(
        default=True, verbose_name=_("Is warehouse active?")
    )

    class Meta:
        """Meta options."""

        verbose_name = _("Warehouse")
        verbose_name_plural = _("Warehouses")
        ordering = ["city", "name"]
        constraints = [
            UniqueConstraint(
                fields=["company", "name"],
                name="uq_warehouse_company_name",
            ),
        ]

    def __str__(self):
        """Returns string representation of an object"""
        return f"{self.name} ({self.city})"
