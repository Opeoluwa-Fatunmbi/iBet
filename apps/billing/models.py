from django.db import models
from apps.core.models import BaseModel
from apps.auth_module.models import CustomUser

# Billing models


class Transaction(BaseModel):
    class TRANSACTION_STATUS_CHOICES(models.TextChoices):
        DEPOSIT = "DEPOSIT", "Deposit"
        WITHDRAWAL = "WITHDRAWAL", "Withdrawal"

    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="transactions"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(
        max_length=20,
        choices=TRANSACTION_STATUS_CHOICES.choices,
        default=TRANSACTION_STATUS_CHOICES.DEPOSIT,
    )
    description = models.CharField(max_length=255, blank=True, null=True)
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    invoice_number = models.CharField(max_length=50, blank=True, null=True)
    is_successful = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.email} - {self.transaction_type} - {self.amount}"

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
