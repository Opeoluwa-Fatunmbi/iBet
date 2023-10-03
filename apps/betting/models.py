from django.db import models
from auth_module.models import CustomUser
from apps.core.models import BaseModel
from django.utils.translation import gettext_laxy as _


class Match(models.Model):
    class STATUS_CHOICES(models.TextChoices):
        SCHEDULED = "SCHEDULED", "Scheduled"
        IN_PROGESS = "IN PROGESS", "In Progress"
        COMPLETED = "COMPLETED", "Completed"

    match_date = models.DateTimeField(
        _("Match Date"), auto_now=False, auto_now_add=False
    )
    game_type = models.CharField(_("Game Type"), max_length=100)
    location = models.CharField(_("Location"), max_length=100)
    status = models.CharField(_("Status"), max_length=20, choices=STATUS_CHOICES)
    winner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="match_winner",
        null=True,
        blank=True,
    )
    loser = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="match_loser",
        null=True,
        blank=True,
    )

    duration_minutes = models.PositiveIntegerField(
        _("Duration (minutes)"), null=True, blank=True
    )
    notes = models.TextField(_("Notes"), blank=True)

    def __str__(self):
        return f"{self.game_type} Match on {self.match_date}"

    class Meta:
        verbose_name = "Match"
        verbose_name_plural = "Matches"


class Bet(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    amount = models.DecimalField(_("Amount"), max_digits=10, decimal_places=2)
    is_winner = models.BooleanField(default=False)

    def __str__(self):
        return f"Bet by {self.user} on {self.match}"

    class Meta:
        verbose_name = "Bet"
        verbose_plural = "Bets"


class Outcome(BaseModel):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    winner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    winning_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.match} - Winner: {self.winner}"

    class Meta:
        verbose_name = "Match"
        verbose_plural = "Matches"
