from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from apps.auth_module.models import User


# Create your tests here.


class TestMediator(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email="testemail@gmail.com",
            full_name="test",
            username="test",
            password="test",
        )
        self.user.save()
