from django.db import models
from apps.auth_module.models import User
from apps.core.models import BaseModel
from django.utils.translation import gettext_lazy as _
from apps.mediation.models import Mediator
from apps.game.models import Player
from apps.game.models import Game


class Match(BaseModel):
    class MATCH_STATUS_CHOICES(models.TextChoices):
        SCHEDULED = "SCHEDULED", _("Scheduled")
        IN_PROGRESS = "IN_PROGRESS", _("In Progress")
        COMPLETED = "COMPLETED", _("Completed")

    status = models.CharField(
        _("Status"),
        max_length=20,
        choices=MATCH_STATUS_CHOICES.choices,
        default=MATCH_STATUS_CHOICES.SCHEDULED,
    )
    player_1 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="match_player_1",
        null=True,
        blank=True,
    )
    player_2 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="match_player_2",
        null=True,
        blank=True,
    )

    duration_minutes = models.PositiveIntegerField(
        _("Duration (minutes)"), null=True, blank=True
    )
    notes = models.TextField(_("Notes"), blank=True)
    mediator = models.OneToOneField(Mediator, on_delete=models.CASCADE, null=True)
    amount = models.DecimalField(
        _("Amount"), max_digits=10, decimal_places=2, default=0
    )
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True)
    is_occupied = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.player_1} vs {self.player_2}"

    class Meta:
        verbose_name = "Match"
        verbose_name_plural = "Matches"


class Bet(BaseModel):
    player_1 = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name="player_bet", default=1
    )
    player_2 = models.ForeignKey(Player, on_delete=models.CASCADE, default=1)
    amount = models.DecimalField(_("Amount"), max_digits=10, decimal_places=2)
    game = models.ForeignKey(
        Game, on_delete=models.CASCADE, related_name="game_bet", default=1
    )

    def __str__(self):
        return f"{self.match} - {self.amount}"

    class Meta:
        verbose_name = "Bet"
        verbose_name_plural = "Bets"


class Outcome(BaseModel):
    match = models.OneToOneField(
        Match, on_delete=models.CASCADE, related_name="outcomes"
    )
    winner = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name="winning_outcomes"
    )
    loser = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name="losing_outcomes", default=None
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.match} - Winner: {self.winner}"

    class Meta:
        verbose_name = "Outcome"
        verbose_name_plural = "Outcomes"
