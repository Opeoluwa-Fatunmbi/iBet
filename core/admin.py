from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(User)
admin.site.register(Game)
admin.site.register(Bet)
admin.site.register(Transaction)
admin.site.register(Mediator)
admin.site.register(Match)
