from django.db import models
from apps.core.models import BaseModel
from apps.auth_module.models import CustomUser
from apps.game.models import Game


# Create your models here.
class Bet(BaseModel):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="user_bet"
    )
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="game_bet")
    stake_amount = models.DecimalField(max_digits=10, decimal_places=2)
    chosen_player = models.ForeignKey(
        CustomUser, related_name="chosen_bets", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.user.username} - {self.game.name}"
