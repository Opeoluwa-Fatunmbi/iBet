from django.contrib import admin
from apps.betting.models import *

# Register your models here.
admin.site.register(Bet)
admin.site.register(Outcome)
admin.site.register(Match)
