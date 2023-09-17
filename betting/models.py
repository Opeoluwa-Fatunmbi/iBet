from django.db import models
from core.models import BaseModel
from user.models import User
from game.models import Game
# Create your models here.
class Bet(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bet")
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="game_bet")
    stake_amount = models.DecimalField(max_digits=10, decimal_places=2)
    chosen_player = models.ForeignKey(User, related_name='chosen_bets', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.game.name}"
