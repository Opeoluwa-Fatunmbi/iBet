from rest_framework import serializers
from apps.billing.models import Transaction, Wallet, Invoice


class TransactionSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = serializers.CharField(max_length=20)
    description = serializers.CharField(max_length=255)
    payment_method = serializers.CharField(max_length=20)
    invoice_number = serializers.CharField(max_length=50)
    is_successful = serializers.BooleanField()

    def create(self, validated_data):
        return Transaction.objects.create(**validated_data)


class WalletSerializer(serializers.Serializer):
    balance = serializers.DecimalField(max_digits=10, decimal_places=2)

    def create(self, validated_data):
        return Wallet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.balance = validated_data.get("balance", instance.balance)
        instance.save()
        return instance


class InvoiceSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    invoice_number = serializers.CharField(max_length=50)
    is_successful = serializers.BooleanField()

    def create(self, validated_data):
        return Invoice.objects.create(**validated_data)
