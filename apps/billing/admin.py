from django.contrib import admin
from apps.billing.models import *

# Register your models here.


class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "amount",
        "transaction_type",
        "payment_method",
        "is_successful",
    )
    list_filter = list_display
    search_fields = ["user__email"]


class WalletAdmin(admin.ModelAdmin):
    list_display = ("user", "balance")
    list_filter = list_display
    search_fields = ["user__email"]


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("user", "amount", "invoice_number", "is_successful")
    list_filter = list_display
    search_fields = ["user__email"]


admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Wallet, WalletAdmin)
admin.site.register(Invoice, InvoiceAdmin)
