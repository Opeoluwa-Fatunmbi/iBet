from django.db import models
from apps.core.models import BaseModel
from apps.auth_module.models import CustomUser

# Create your models here.


class Transaction(BaseModel):
    TRANSACTION_TYPES = (
        ("stake", "Stake"),
        ("winnings", "Winnings"),
    )
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="transactions"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} - {self.amount}"
