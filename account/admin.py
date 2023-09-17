from django.contrib import admin
from . models import User, PaymentTransaction, Withdraw
# Register your models here.

admin.site.register(User)
admin.site.register(PaymentTransaction)
admin.site.register(Withdraw)