from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser
from cloudinary.models import CloudinaryField
from apps.core.models import BaseModel
from django.utils.translation import gettext_lazy as _
from apps.user.managers import CustomUserManager

# Create your models here.


class User(BaseModel, PermissionsMixin, AbstractBaseUser):
    profile_pic = CloudinaryField(_("image"),default=None, null=True)
    email = models.EmailField(_('email address'), blank=False, unique=True)
    first_name = models.CharField(_("first_name"), max_length=50, blank=True)
    last_name = models.CharField(_("last_name"), max_length=50)
    is_email_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    terms_agreement = models.BooleanField(default=False)
    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")


