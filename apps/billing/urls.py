from django.urls import path
from apps.billing.views import WalletView, TransactionView, InvoiceView

app_name = "apps.billing"


urlpatterns = [
    path("wallet/", WalletView.as_view(), name="wallet"),
    path("transactions/", TransactionView.as_view(), name="transactions"),
    path("invoice/", InvoiceView.as_view(), name="invoice"),
]
