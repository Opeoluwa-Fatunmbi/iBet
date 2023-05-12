
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    # Add unique related_name arguments to avoid clashes with Django's built-in User model
    groups = models.ManyToManyField('auth.Group', related_name='api_users')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='api_users')


class Game(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    category = models.CharField(max_length=50)



class Bet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bet")
    game = models.ForeignKey(Game, on_delete=models.CASCADE,  related_name="game_bet")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)


class Mediator(models.Model):
    mediator_user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,  related_name="user_transaction")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_time = models.DateTimeField(auto_now_add=True)



class UserContact(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_contact")
    phone_number = models.CharField(max_length=20)
