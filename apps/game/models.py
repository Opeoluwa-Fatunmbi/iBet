from django.db import models
from auth_module.models import CustomUser
from django.utils.translation import gettext_lazy as _
from apps.core.models import BaseModel


class Game(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=150)
    rules = models.TextField(_("Rules"), max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Game"
        verbose_plural = "Games"


class Player(BaseModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    # score,
    # game-specific data

    def __str__(self):
        return self.user

    class Meta:
        verbose_name = "Player"
        verbose_plural = "Players"
