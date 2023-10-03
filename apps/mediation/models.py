from django.db import models
from auth_module.models import CustomUser
from betting.models import Bet
from apps.core.models import BaseModel
from django.utils.translation import gettext_lazy as _


# Mediation models
class Mediator(BaseModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    mediation_experience = models.PositiveIntegerField(default=0)
    fees = models.DecimalField(_("Fees"), max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.user

    class Meta:
        verbose_name = _("Mediator")
        verbose_name_plural = _("Mediators")


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
        verbose_name = _("Mediation")
        verbose_name_plural = _("Mediations")
