from django.db import models
from apps.core.models import BaseModel
from apps.auth_module.models import User
from django.utils.translation import gettext_lazy as _

# Billing models


class Transaction(BaseModel):
    class TRANSACTION_STATUS_CHOICES(models.TextChoices):
        DEPOSIT = "DEPOSIT", _("Deposit")
        WITHDRAWAL = "WITHDRAWAL", _("Withdrawal")
        REFUND = "REFUND", _("Refund")
        PENDING = "PENDING", _("Pending")

    class PAYMENT_METHOD_CHOICES(models.TextChoices):
        PAYPAL = "PAYPAL", _("PayPal")
        CREDIT_CARD = "CREDIT_CARD", _("Credit Card")
        BANK_TRANSFER = "BANK_TRANSFER", _("Bank Transfer")

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="transactions"
    )
    amount = models.PositiveIntegerField(default=0)
    transaction_type = models.CharField(
        max_length=20,
        choices=TRANSACTION_STATUS_CHOICES.choices,
        default=TRANSACTION_STATUS_CHOICES.DEPOSIT,
    )
    description = models.CharField(max_length=255, blank=True, null=True)
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES.choices,
        default=PAYMENT_METHOD_CHOICES.BANK_TRANSFER,
    )
    is_successful = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.email} - {self.transaction_type} - {self.amount}"

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"


class Wallet(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="wallet")
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = "Wallet"
        verbose_name_plural = "Wallets"


class Invoice(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="invoices")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    invoice_number = models.CharField(max_length=50, blank=True, null=True)
    is_successful = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.email} - {self.invoice_number} - {self.amount}"

    class Meta:
        verbose_name = "Invoice"
        verbose_name_plural = "Invoices"
