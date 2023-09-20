from django.contrib import admin
from apps.user.models import User
from django.contrib.auth.admin import UserAdmin
# Register your models here.



class UserAdminConfig(UserAdmin):
    search_fields = ('email',)
    ordering = ('-created_at',)
    list_display = ('email', 'is_active', 'is_staff')

admin.site.register(User, UserAdminConfig)
