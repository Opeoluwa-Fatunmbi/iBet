from django.contrib.auth.base_user import BaseUserManager
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _
from django.db import models
from apps.auth_module.models import CustomUser


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        # extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff set to True"))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser set to True."))
        return self.create_user(email=email, password=password, **extra_fields)


class PlayerManager(models.Manager):
    def get_queryset(self, *args, **kwargs) -> QuerySet:
        return (
            super().get_queryset(*args, **kwargs).filter(type=CustomUser.Types.PLAYER)
        )


class MediatorManager(models.Manager):
    def get_queryset(self, *args, **kwargs) -> QuerySet:
        return (
            super().get_queryset(*args, **kwargs).filter(type=CustomUser.Types.MEDIATOR)
        )
