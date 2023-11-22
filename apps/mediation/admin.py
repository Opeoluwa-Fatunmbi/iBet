from django.contrib import admin
from apps.mediation.models import Mediator, Mediation


class MediatorAdmin(admin.ModelAdmin):
    list_display = ("user", "is_active", "created_at", "updated_at")
    list_filter = list_display
    search_fields = ("is_active", "created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")


class MediationAdmin(admin.ModelAdmin):
    list_display = ("created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")


admin.site.register(Mediation, MediationAdmin)
admin.site.register(Mediator, MediatorAdmin)
