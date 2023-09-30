from django.db import models
from auth_module.models import CustomUser
from django.utils.translation import gettext_lazy as _
from apps.core.models import BaseModel


class Game(BaseModel):
    class Games(models.TextChoices):
        EIGHTBALL = "8BALL", "8Ball"
        NINEBALL = "9BALL", "9Ball"
        SEABATTLE = "SEABATTLE", "SeaBattle"
        BASKETBALL = "BASKETBALL", "Basketball"
        GOLF = "GOLF", "Golf"
        CUPPONG = "CUPPONG", "Cuppong"
        DARTS = "DARTS", "Darts"
        FOURINAROW = "FOURINAROW", "Fourinarow"
        ARCHERY = "ARCHERY", "Archery"
        WORDHUNT = "WORDHUNT", "Wordhunt"
        ANAGRAMS = "ANAGRAMS", "Anagrams"
        WORDBITES = "WORDBITES", "Wordbites"

    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    rules = models.TextField(_("Rules"), max_length=500)
    game = models.CharField(
        _("Rules"), max_length=50, choices=Games.choices, default=Games.EIGHTBALL
    )
    goal = models.TextField(_("Goal"), max_length=200)

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
