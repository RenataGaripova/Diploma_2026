# Python modules
from typing import Any

# Django modules
from django.db.models import (
    Model,
    Manager,
    QuerySet,
    DateTimeField,
)
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class AbstractBaseModel(Model):
    """Abstract Base Model with common fields."""

    created_at = DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        """Meta class."""

        abstract = True


class SoftDeleteQuerySet(QuerySet):
    """QuerySet whose delete() marks rows as deleted instead of removing them."""

    def delete(self) -> int:
        """Soft deletes all objects in the queryset."""
        now = timezone.now()
        return self.update(deleted_at=now, updated_at=now)

    def hard_delete(self) -> tuple[int, dict[str, int]]:
        """Permanently removes all objects in the queryset."""
        return super().delete()

    def restore(self) -> int:
        """Restores all soft deleted objects in the queryset."""
        return self.update(deleted_at=None, updated_at=timezone.now())

    def alive(self) -> "SoftDeleteQuerySet":
        """Returns objects that are not deleted."""
        return self.filter(deleted_at__isnull=True)

    def deleted(self) -> "SoftDeleteQuerySet":
        """Returns soft deleted objects."""
        return self.filter(deleted_at__isnull=False)


class SoftDeleteManager(Manager.from_queryset(SoftDeleteQuerySet)):
    """Manager that hides soft deleted objects."""

    def get_queryset(self) -> SoftDeleteQuerySet:
        """Returns only objects that are not deleted."""
        return super().get_queryset().alive()


class AbstractSoftDeleteModel(AbstractBaseModel):
    """Abstract Base Model with soft delete support."""

    deleted_at = DateTimeField(
        null=True,
        blank=True,
        db_index=True,
        verbose_name=_("Deleted at"),
    )

    objects = SoftDeleteManager()
    all_objects = Manager.from_queryset(SoftDeleteQuerySet)()

    class Meta:
        """Meta class."""

        abstract = True

    @property
    def is_deleted(self) -> bool:
        """Returns True if the object is soft deleted."""
        return self.deleted_at is not None

    def delete(self, *args: Any, **kwargs: Any) -> None:
        """Soft deletes the object."""
        self.deleted_at = timezone.now()
        self.save(update_fields=["deleted_at", "updated_at"])

    def hard_delete(
        self, *args: Any, **kwargs: Any
    ) -> tuple[int, dict[str, int]]:
        """Permanently removes the object from the database."""
        return super().delete(*args, **kwargs)

    def restore(self) -> None:
        """Restores the soft deleted object."""
        self.deleted_at = None
        self.save(update_fields=["deleted_at", "updated_at"])
