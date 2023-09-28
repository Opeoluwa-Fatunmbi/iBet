from django.db import models
from auth_module.models import CustomUser
from betting.models import Bet
from apps.core.models import BaseModel
from django.utils.translation import gettext_lazy as _


class Mediator(BaseModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    # mediation experience,
    # fees, etc.
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Mediator")
        verbose_name_plural = _("Mediators")


class Mediation(BaseModel):
    bet = models.OneToOneField(Bet, on_delete=models.CASCADE)
    mediator = models.ForeignKey(Mediator, on_delete=models.CASCADE)
    # mediation status,
    #  results, etc.

    def __str__(self):
        return self.mediator

    class Meta:
        verbose_name = _("Mediation")
        verbose_name_plural = _("Mediations")
