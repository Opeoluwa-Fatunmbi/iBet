"""
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['created']),
            models.Index(fields=['updated']),
        ]

"""

from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    phone_number = models.CharField(max_length=20)

    groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        related_name='custom_user_groups',
        related_query_name='custom_user_group',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        related_name='custom_user_permissions',
        related_query_name='custom_user_permission',
    )

    class Meta:
        indexes = [
            models.Index(fields=['created']),
            models.Index(fields=['updated']),
        ]
















class Game(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    category = models.CharField(max_length=50)

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['category']),
        ]


class Bet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bet")
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="game_bet")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)

    class Meta:
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['game']),
            models.Index(fields=['amount']),
            models.Index(fields=['status']),
        ]


class Mediator(models.Model):
    mediator_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mediator_user")
    name = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)

    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_transaction")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['amount']),
            models.Index(fields=['date_time']),
        ]


class UserContact(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_contact")
    phone_number = models.CharField(max_length=20)

    class Meta:
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['phone_number']),
        ]
