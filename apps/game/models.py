from django.db import models
from apps.auth_module.models import User
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

    name = models.CharField(
        _("Game"), max_length=50, choices=Games.choices, default=Games.EIGHTBALL
    )
    description = models.TextField(max_length=500)
    rules = models.TextField(_("Rules"), max_length=500)
    goal = models.TextField(_("Goal"), max_length=200)
    min_players = models.PositiveIntegerField(default=2)
    max_players = models.PositiveIntegerField(default=3)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Game"
        verbose_name_plural = "Games"


class Player(BaseModel):
    class ExperienceLevel(models.TextChoices):
        BEGINNER = "BEGINNER", _("Beginner")
        INTERMEDIATE = "INTERMEDIATE", _("Intermediate")
        MASTER = "MASTER", _("Master")

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="player")
    experience_level = models.CharField(
        _("Experience Level"),
        max_length=50,
        choices=ExperienceLevel.choices,
        default=ExperienceLevel.BEGINNER,
    )

    def __str__(self):
        return f"{self.user.full_name}"

    class Meta:
        verbose_name = "Player"
        verbose_name_plural = "Players"
