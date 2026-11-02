# Python modules
from typing import Any

# Django modules
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db.models import (
    CharField,
    EmailField,
    BooleanField,
)
from django.utils.translation import gettext_lazy as _

# Project modules
from apps.abstracts.models import AbstractBaseModel


class CustomUserManager(BaseUserManager):
    """Custom user manager."""

    def create_user(
        self,
        email: str,
        first_name: str,
        last_name: str,
        password: str,
        **kwargs: dict[Any, Any],
    ) -> "CustomUser":
        """Creates and saves a User with the given data."""

        if not email:
            raise ValueError(_("Users must have an email address"))
        if not first_name:
            raise ValueError(_("Users must have a first name"))
        if not last_name:
            raise ValueError(_("Users must have a last name"))

        created_user: "CustomUser" = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            **kwargs,
        )
        created_user.set_password(password)
        created_user.save(using=self._db)
        return created_user

    def create_superuser(
        self,
        email: str,
        first_name: str,
        last_name: str,
        password: str,
        **kwargs: dict[Any, Any],
    ) -> "CustomUser":
        """Creates and saves a Super user with the given data."""

        kwargs.setdefault("is_active", True)
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)

        if kwargs.get("is_active") is not True:
            raise ValueError(_("is_active should be True for superuser"))
        if kwargs.get("is_staff") is not True:
            raise ValueError(_("is_staff should be True for superuser"))
        if kwargs.get("is_superuser") is not True:
            raise ValueError(_("is_superuser should be True for superuser"))

        return self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            **kwargs,
        )


class CustomUser(AbstractBaseUser, PermissionsMixin, AbstractBaseModel):
    """
    CustomUser database (table) model.
    """

    MAX_FIRST_NAME_LENGTH = 64
    MAX_LAST_NAME_LENGTH = 64
    MAX_EMAIL_LENGTH = 64
    MAX_PASSWORD_LENGTH = 128

    email = EmailField(
        max_length=MAX_EMAIL_LENGTH,
        unique=True,
        verbose_name=_("Email"),
    )
    first_name = CharField(
        max_length=MAX_FIRST_NAME_LENGTH,
        verbose_name=_("First name"),
    )
    last_name = CharField(
        max_length=MAX_LAST_NAME_LENGTH,
        verbose_name=_("Last name"),
    )
    is_active = BooleanField(default=True, verbose_name=_("Is user active?"))
    is_staff = BooleanField(default=False, verbose_name=_("Is staff?"))

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        """Meta options for CustomUser model."""

        verbose_name = _("Custom User")
        verbose_name_plural = _("Custom Users")
        ordering = ["-created_at"]

    def __str__(self):
        """Returns string representation of an object"""
        return self.email
