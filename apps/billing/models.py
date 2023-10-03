from django.db import models
from apps.core.models import BaseModel
from apps.auth_module.models import CustomUser

# Billing models


class Transaction(BaseModel):
    class TRANSACTION_TYPES(models.TextChoices):
        STAKE = "STAKE", "Stake"
        WINNINGS = "WINNINGS", "Winnings"

    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="transactions"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    description = models.CharField(max_length=255, blank=True, null=True)
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    invoice_number = models.CharField(max_length=50, blank=True, null=True)
    is_successful = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.email} - {self.transaction_type} - {self.amount}"
