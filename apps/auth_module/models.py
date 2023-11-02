from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from apps.auth_module.managers import CustomUserManager
from apps.core.models import BaseModel
from django.conf import settings
from django.utils import timezone
import uuid


class CustomUser(AbstractBaseUser, PermissionsMixin):
    class ROLES_CHOICES(models.TextChoices):
        PLAYER = "PLAYER", _("Player")
        MEDIATOR = "MEDIATOR", _("Mediator")

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, unique=True, editable=False
    )
    role = models.CharField(
        _("Role Choices"),
        max_length=50,
        choices=ROLES_CHOICES.choices,
        default=ROLES_CHOICES.PLAYER,
    )
    username = None
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(max_length=50, default="John")
    last_name = models.CharField(max_length=50, default="Doe")
    date_of_birth = models.DateField(_("date of birth"), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_email_verified = models.BooleanField(default=False)
    terms_agreement = models.BooleanField(default=False)

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
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.email

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Jwt(BaseModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    access = models.TextField()
    refresh = models.TextField()
    blacklisted = models.BooleanField(default=False)


class Otp(BaseModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    code = models.IntegerField()

    def check_expiration(self):
        now = timezone.now()
        diff = now - self.updated_at
        if diff.total_seconds() > int(settings.EMAIL_OTP_EXPIRE_SECONDS):
            return True
        return False
