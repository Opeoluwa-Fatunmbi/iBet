from django.db import models
from apps.auth_module.models import User
from apps.betting.models import Bet
from apps.core.models import BaseModel
from django.utils.translation import gettext_lazy as _


# Mediation models
class Mediator(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mediation_experience = models.PositiveIntegerField(default=0)
    fees = models.DecimalField(_("Fees"), max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.user

    class Meta:
        verbose_name = "Mediator"
        verbose_name_plural = "Mediators"


class Mediation(BaseModel):
    bet = models.OneToOneField(Bet, on_delete=models.CASCADE)
    mediator = models.ForeignKey(Mediator, on_delete=models.CASCADE)
    mediation_status = models.CharField(
        _("Mediation Status"), max_length=50, default="Pending"
    )
    mediation_results = models.TextField(_("Mediation Results"), blank=True)

    def __str__(self):
        return self.mediator

    class Meta:
        verbose_name = "Mediation"
        verbose_name_plural = "Mediations"
