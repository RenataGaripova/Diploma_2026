# Python modules
import re
from typing import Any

# Django modules
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db.models import (
    PROTECT,
    SET_NULL,
    BooleanField,
    CharField,
    CheckConstraint,
    EmailField,
    ForeignKey,
    Index,
    Q,
    TextChoices,
)
from django.utils.translation import gettext_lazy as _

# Project modules
from apps.abstracts.models import AbstractBaseModel


class CustomUserManager(BaseUserManager):
    """Custom user manager."""

    @classmethod
    def normalize_phone(cls, phone: str) -> str:
        """Brings phone number to +7XXXXXXXXXX format."""
        digits = re.sub(r"\D", "", phone or "")
        if len(digits) == 11 and digits.startswith("8"):
            digits = "7" + digits[1:]
        return f"+{digits}" if digits else ""

    def get_by_natural_key(self, username: str) -> "CustomUser":
        """Finds user by phone regardless of its input format."""
        return super().get_by_natural_key(self.normalize_phone(username))

    def create_user(
        self,
        phone: str,
        first_name: str,
        last_name: str,
        password: str,
        **kwargs: dict[Any, Any],
    ) -> "CustomUser":
        """Creates and saves a User with the given data."""

        if not phone:
            raise ValueError(_("Users must have a phone number"))
        if not first_name:
            raise ValueError(_("Users must have a first name"))
        if not last_name:
            raise ValueError(_("Users must have a last name"))

        email = kwargs.pop("email", None)
        created_user: "CustomUser" = self.model(
            phone=self.normalize_phone(phone),
            email=self.normalize_email(email) if email else None,
            first_name=first_name,
            last_name=last_name,
            **kwargs,
        )
        created_user.set_password(password)
        created_user.save(using=self._db)
        return created_user

    def create_superuser(
        self,
        phone: str,
        first_name: str,
        last_name: str,
        password: str,
        **kwargs: dict[Any, Any],
    ) -> "CustomUser":
        """Creates and saves a Super user (platform admin) with the given data."""

        kwargs.setdefault("is_active", True)
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("role", CustomUser.Role.PLATFORM_ADMIN)

        if kwargs.get("is_active") is not True:
            raise ValueError(_("is_active should be True for superuser"))
        if kwargs.get("is_staff") is not True:
            raise ValueError(_("is_staff should be True for superuser"))
        if kwargs.get("is_superuser") is not True:
            raise ValueError(_("is_superuser should be True for superuser"))
        if kwargs.get("role") != CustomUser.Role.PLATFORM_ADMIN:
            raise ValueError(_("Superuser must have platform admin role"))

        return self.create_user(
            phone=phone,
            first_name=first_name,
            last_name=last_name,
            password=password,
            **kwargs,
        )


class CustomUser(AbstractBaseUser, PermissionsMixin, AbstractBaseModel):
    """
    CustomUser database (table) model.
    """

    class Role(TextChoices):
        """User roles in the system."""

        PLATFORM_ADMIN = "platform_admin", _("Platform admin")
        ADMIN = "admin", _("Company admin")
        WAREHOUSE_MANAGER = "warehouse_manager", _("Warehouse manager")
        SELLER = "seller", _("Seller")

    # Roles that work without a company / without a warehouse
    ROLES_WITHOUT_COMPANY = (Role.PLATFORM_ADMIN,)
    ROLES_WITHOUT_WAREHOUSE = (Role.PLATFORM_ADMIN, Role.ADMIN)

    MAX_PHONE_LENGTH = 16
    MAX_FIRST_NAME_LENGTH = 64
    MAX_LAST_NAME_LENGTH = 64
    MAX_JOB_TITLE_LENGTH = 128
    MAX_EMAIL_LENGTH = 64
    MAX_ROLE_LENGTH = 32
    MAX_PASSWORD_LENGTH = 128

    phone = CharField(
        max_length=MAX_PHONE_LENGTH,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^\+\d{10,15}$",
                message=_("Phone number must be in format +7XXXXXXXXXX"),
            )
        ],
        verbose_name=_("Phone"),
    )
    email = EmailField(
        max_length=MAX_EMAIL_LENGTH,
        unique=True,
        null=True,
        blank=True,
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
    job_title = CharField(
        max_length=MAX_JOB_TITLE_LENGTH,
        blank=True,
        verbose_name=_("Job title"),
    )
    role = CharField(
        max_length=MAX_ROLE_LENGTH,
        choices=Role.choices,
        verbose_name=_("Role"),
    )
    company = ForeignKey(
        "companies.Company",
        on_delete=PROTECT,
        null=True,
        blank=True,
        related_name="users",
        verbose_name=_("Company"),
    )
    warehouse = ForeignKey(
        "companies.Warehouse",
        on_delete=PROTECT,
        null=True,
        blank=True,
        related_name="employees",
        verbose_name=_("Warehouse"),
    )
    created_by = ForeignKey(
        "self",
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name=_("Created by"),
    )
    is_active = BooleanField(default=True, verbose_name=_("Is user active?"))
    is_staff = BooleanField(default=False, verbose_name=_("Is staff?"))

    objects = CustomUserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        """Meta options for CustomUser model."""

        verbose_name = _("Custom User")
        verbose_name_plural = _("Custom Users")
        ordering = ["-created_at"]
        indexes = [
            Index(fields=["company", "role"]),
            Index(fields=["warehouse", "role"]),
        ]
        constraints = [
            # platform admin has no company, everyone else must have one
            CheckConstraint(
                condition=(
                    Q(role="platform_admin", company__isnull=True)
                    | (~Q(role="platform_admin") & Q(company__isnull=False))
                ),
                name="chk_user_company",
            ),
            # warehouse managers and sellers must be bound to a warehouse
            CheckConstraint(
                condition=(
                    Q(role__in=["platform_admin", "admin"])
                    | Q(warehouse__isnull=False)
                ),
                name="chk_user_warehouse",
            ),
        ]

    def __str__(self):
        """Returns string representation of an object"""
        return f"{self.full_name} ({self.phone})"

    @property
    def full_name(self) -> str:
        """Returns last name and first name of the user."""
        return f"{self.last_name} {self.first_name}"

    def clean_fields(self, exclude: Any = None) -> None:
        """Normalizes phone and email before field validators run."""
        self.phone = CustomUser.objects.normalize_phone(self.phone)
        if not self.email:
            self.email = None
        super().clean_fields(exclude=exclude)

    def clean(self) -> None:
        """Validates role, company and warehouse consistency."""
        super().clean()

        errors: dict[str, str] = {}
        if self.role in self.ROLES_WITHOUT_COMPANY:
            if self.company_id:
                errors["company"] = _("Platform admin can not belong to a company")
            if self.warehouse_id:
                errors["warehouse"] = _("Platform admin can not have a warehouse")
        elif not self.company_id:
            errors["company"] = _("Company is required for this role")

        if self.role not in self.ROLES_WITHOUT_WAREHOUSE and not self.warehouse_id:
            errors["warehouse"] = _("Warehouse is required for this role")
        # Django has no composite foreign keys, so check tenant isolation here
        if (
            self.warehouse_id
            and self.company_id
            and self.warehouse.company_id != self.company_id
        ):
            errors["warehouse"] = _("Warehouse belongs to another company")

        if errors:
            raise ValidationError(errors)
