from django.db import models
from auth_module.models import CustomUser
from apps.core.models import BaseModel
from django.utils.translation import gettext_laxy as _


class Match(BaseModel):
    # Fields for a match
    # match_date,
    # game_type, etc.
    pass


class Bet(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    amount = models.DecimalField(_("Amount"), max_digits=10, decimal_places=2)

    def __str__(self):
        return self.user

    class Meta:
        verbose_name = "Bet"
        verbose_plural = "Bets"


class Outcome(BaseModel):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    winner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    # winning amount,
    #  status, etc.
    def __str__(self):
        return self.match

    class Meta:
        verbose_name = "Match"
        verbose_plural = "Matches"
