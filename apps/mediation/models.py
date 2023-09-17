from django.db import models
from apps.core.models import BaseModel
from apps.user.models import User

# Create your models here.
class Mediator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="game_mediator")

    def __str__(self):
        return self.user.username