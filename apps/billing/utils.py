import uuid
from django.utils.translation import gettext_lazy as _
from apps.billing.models import Wallet


def get_billing_user(user):
    """
    Get user wallet
    """
    try:
        wallet = Wallet.objects.get(user=user)
    except Wallet.DoesNotExist:
        wallet = Wallet.objects.create(user=user)
    return wallet


def generate_invoice_number():
    """
    Generate invoice number
    """
    return str(uuid.uuid4()).replace("-", "")[:50]
