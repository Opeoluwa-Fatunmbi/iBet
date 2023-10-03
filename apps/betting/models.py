from django.db import models
from apps.auth_module.models import CustomUser
from apps.core.models import BaseModel
from django.utils.translation import gettext_lazy as _


class Match(models.Model):
    class MATCH_STATUS_CHOICES(models.TextChoices):
        SCHEDULED = "SCHEDULED", _("Scheduled")
        IN_PROGRESS = "IN_PROGRESS", _("In Progress")
        COMPLETED = "COMPLETED", _("Completed")

    match_date = models.DateTimeField(
        _("Match Date"), auto_now=False, auto_now_add=False
    )
    game_type = models.CharField(_("Game Type"), max_length=100)
    location = models.CharField(_("Location"), max_length=100)
    status = models.CharField(
        _("Status"),
        max_length=20,
        choices=MATCH_STATUS_CHOICES.choices,
        default=MATCH_STATUS_CHOICES.SCHEDULED,
    )
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
        verbose_name_plural = "Bets"


class Outcome(BaseModel):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    winner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    winning_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.match} - Winner: {self.winner}"

    class Meta:
        verbose_name = "Match"
        verbose_name_plural = "Matches"
