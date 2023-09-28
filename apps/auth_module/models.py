from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager, PlayerManager, MediatorManager
import uuid


class CustomUser(AbstractBaseUser, PermissionsMixin):
    class Roles(models.TextChoices):
        PLAYER = "PLAYER", "Player"
        MEDIATOR = "MEDIATOR", "Mediator"

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, unique=True, editable=False
    )
    role = models.CharField(
        _("Type"), max_length=50, choices=Roles.choices, default=Roles.PLAYER
    )
    username = None
    email = models.EmailField(_("email address"), unique=True)
    full_name = models.CharField(_("full name"), max_length=150)
    date_of_birth = models.DateField(_("date of birth"), null=True, blank=True)
    confirm_email_token = models.UUIDField(default=uuid.uuid4, null=True)
    reset_password_token = models.UUIDField(default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_superuser = models.BooleanField(
        _("superuser status"),
        default=False,
        help_text=_("Designates whether the user has all permissions."),
    )

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Staff status"),
    )

    def __str__(self) -> str:
        return self.email
