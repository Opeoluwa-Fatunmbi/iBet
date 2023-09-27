from django.contrib import admin
from apps.auth_module.models import CustomUser

# Register your models here.


admin.site.register(CustomUser)
