from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from apps.auth_module.models import User
from apps.billing.models import Wallet, Transaction


# Create your tests here.


class TestBilling(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email="testemail.com@gmail.com",
            full_name="test",
            username="test",
            password="test",
        )
        self.user.save()
        self.wallet = Wallet.objects.create(
            user=self.user,
            balance=1000,
        )
        self.wallet.save()

    def test_get_wallet(self):
        """
        Ensure we can get wallet
        """
        url = reverse("billing:wallet")
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["balance"], 1000)

    def test_get_transaction(self):
        """
        Ensure we can get transaction
        """
        url = reverse("billing:transaction")
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_post_transaction(self):
        """
        Ensure we can post transaction
        """
        url = reverse("billing:transaction")
        self.client.force_authenticate(user=self.user)
        data = {"amount": 100, "type": "deposit"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["amount"], 100)
        self.assertEqual(response.data["type"], "deposit")
        self.assertEqual(response.data["wallet"], self.wallet.id)
        self.assertEqual(response.data["wallet_balance"], 1100)

    def test_post_transaction_withdraw(self):
        """
        Ensure we can post transaction
        """
        url = reverse("billing:transaction")
        self.client.force_authenticate(user=self.user)
        data = {"amount": 100, "type": "withdraw"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["amount"], 100)
        self.assertEqual(response.data["type"], "withdraw")
        self.assertEqual(response.data["wallet"], self.wallet.id)
        self.assertEqual(response.data["wallet_balance"], 900)
