from django.contrib import admin
from . models import LotteryDraw, LotteryTicket, Game
# Register your models here.

admin.site.register(Game)
admin.site.register(LotteryDraw)
admin.site.register(LotteryTicket)