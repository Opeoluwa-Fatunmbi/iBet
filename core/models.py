from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField

class User(AbstractUser):
    profile_pic = CloudinaryField("image",default=None,null=True)

class Game(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return self.name

class Bet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bet")
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="game_bet")
    stake_amount = models.DecimalField(max_digits=10, decimal_places=2)
    chosen_player = models.ForeignKey(User, related_name='chosen_bets', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.game.name}"

class Mediator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="game_mediator")

    def __str__(self):
        return self.user.username

class Match(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player1 = models.ForeignKey(User, related_name='matches_as_player1', on_delete=models.CASCADE)
    player2 = models.ForeignKey(User, related_name='matches_as_player2', on_delete=models.CASCADE)
    mediator = models.ForeignKey(Mediator, on_delete=models.CASCADE)
    winner = models.ForeignKey(User, related_name='won_matches', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.player1.username} vs {self.player2.username} - {self.game.name}"

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('stake', 'Stake'),
        ('winnings', 'Winnings'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} - {self.amount}"
