from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.auth_module.models import User
from apps.core.models import BaseModel


# Mediation models
class Mediator(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)  # or return self.user.username

    class Meta:
        verbose_name = "Mediator"
        verbose_name_plural = "Mediators"


class Mediation(BaseModel):
    class MediationStatus(models.TextChoices):
        PENDING = "PENDING", _("Pending")
        ACCEPTED = "ACCEPTED", _("Accepted")
        REJECTED = "REJECTED", _("Rejected")
        COMPLETED = "COMPLETED", _("Completed")

    mediator = models.ForeignKey(Mediator, on_delete=models.CASCADE)
    status = models.CharField(
        _("Status"),
        max_length=10,
        choices=MediationStatus.choices,
        default=MediationStatus.PENDING,
    )
    mediation_results = models.TextField(_("Mediation Results"), blank=True)

    def __str__(self):
        return str(self.mediator)

    class Meta:
        verbose_name = "Mediation"
        verbose_name_plural = "Mediations"


class Rating(BaseModel):
    class RatingChoices(models.IntegerChoices):
        ONE = 1, _("1")
        TWO = 2, _("2")
        THREE = 3, _("3")
        FOUR = 4, _("4")
        FIVE = 5, _("5")

    mediation = models.ForeignKey(Mediation, on_delete=models.CASCADE)
    rating = models.IntegerField(
        _("Rating"), choices=RatingChoices.choices, default=RatingChoices.ONE
    )
    comments = models.TextField(_("Comments"), blank=True)

    def __str__(self):
        return str(self.mediation)

    class Meta:
        verbose_name = "Rating"
        verbose_name_plural = "Ratings"
