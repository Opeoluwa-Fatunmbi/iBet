from django.shortcuts import render
from apps.billing.models import Wallet, Invoice, Transaction
from rest_framework.views import APIView
from apps.billing.serializers import (
    WalletSerializer,
    TransactionSerializer,
    InvoiceSerializer,
)
from apps.billing.utils import get_billing_user, generate_invoice_number
from apps.core.responses import CustomResponse
from rest_framework import status
from django.utils.translation import gettext_lazy as _
from django.db import transaction
from django.conf import settings
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from apps.billing.emails import Util


# Create your views here.


class WalletView(APIView):
    """
    Wallet view
    """

    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    @extend_schema(description="Get wallet balance", responses={200: WalletSerializer})
    def get(self, request):
        """
        Get wallet balance
        """
        try:
            wallet = get_billing_user(request.user)
            serializer = WalletSerializer(wallet)
            return CustomResponse.success(
                data=serializer.data,
                message=_("Wallet balance"),
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return CustomResponse.error(
                message=_("Error getting wallet balance"),
                errors=e,
                status=400,
            )


class TransactionView(APIView):
    """
    Transaction view
    """

    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    @extend_schema(
        description="Get user transactions", responses={200: TransactionSerializer}
    )
    def get(self, request):
        """
        Get user transactions
        """
        try:
            transactions = Transaction.objects.filter(user=request.user)
            serializer = TransactionSerializer(transactions, many=True)
            return CustomResponse.success(
                data=serializer.data,
                message=_("User transactions"),
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return CustomResponse.error(
                message=_("Error getting user transactions"),
                errors=e,
                status=400,
            )

    @extend_schema(
        description="Create transaction", responses={200: TransactionSerializer}
    )
    def post(self, request):
        """
        Create transaction
        """
        try:
            with transaction.atomic():
                wallet = get_billing_user(request.user)
                serializer = TransactionSerializer(data=request.data)

                serializer.is_valid(raise_exception=True)

                transaction_type = serializer.validated_data.get("transaction_type")
                amount = serializer.validated_data.get("amount")
                payment_method = serializer.validated_data.get("payment_method")
                description = serializer.validated_data.get("description")
                invoice_number = generate_invoice_number()

                if transaction_type == "DEPOSIT":
                    wallet.balance += amount
                else:
                    wallet.balance -= amount
                wallet.save()
                transaction = Transaction.objects.create(
                    user=request.user,
                    amount=amount,
                    transaction_type=transaction_type,
                    payment_method=payment_method,
                    description=description,
                    invoice_number=invoice_number,
                    is_successful=True,
                )
                return CustomResponse.success(
                    data=TransactionSerializer(transaction).data,
                    message=_("Transaction created successfully"),
                    status=status.HTTP_201_CREATED,
                )
        except Exception as e:
            return CustomResponse.error(
                message=_("Error creating transaction"),
                errors=e,
                status=400,
            )


class InvoiceView(APIView):
    """
    Invoice view
    """

    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    @extend_schema(description="Get user invoices", responses={200: InvoiceSerializer})
    def get(self, request):
        """
        Get user invoices
        """
        try:
            invoices = Invoice.objects.filter(user=request.user)
            serializer = InvoiceSerializer(invoices, many=True)
            serializer.is_valid(raise_exception=True)

            Util.send_invoice(request.user)

            return CustomResponse.success(
                data=serializer.data,
                message=_("User invoices"),
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return CustomResponse.error(
                message=_("Error getting user invoices"),
                errors=e,
                status=400,
            )
