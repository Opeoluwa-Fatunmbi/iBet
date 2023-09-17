from django.db import models
from apps.core.models import BaseModel

# Create your models here.



class Game(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return self.name

