from django.contrib import admin
from apps.auth_module.models import User, Jwt, Otp
from django.utils.translation import gettext_lazy as _


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "is_email_verified", "created_at"]
    list_filter = list_display

    fieldsets = (
        (_("Login Credentials"), {"fields": ("email", "password")}),
        (_("Personal Information"), {"fields": ("first_name", "last_name", "avatar")}),
        (
            _("Permissions and Groups"),
            {
                "fields": (
                    "is_email_verified",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important Dates"), {"fields": ("created_at", "updated_at", "last_login")}),
    )

    readonly_fields = ("created_at", "updated_at")


class JwtAdmin(admin.ModelAdmin):
    list_display = ("user", "blacklisted", "created_at")
    list_filter = list_display
    search_fields = ["user__email", "user__first_name", "user__last_name"]
    list_filter = ["blacklisted"]


class OtpAdmin(admin.ModelAdmin):
    list_display = ("user", "code", "created_at")
    list_filter = list_display
    search_fields = ["user__email", "user__first_name", "user__last_name"]


admin.site.register(User, UserAdmin)
admin.site.register(Jwt, JwtAdmin)
admin.site.register(Otp, OtpAdmin)
