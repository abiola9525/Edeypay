from django.db import models
from account.models import User
from django.conf import settings
from django.core.validators import validate_comma_separated_integer_list


# Create your models here.
class LotteryEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_number = models.IntegerField()
    second_number = models.IntegerField()
    amount = models.FloatField(default=0.0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - Numbers: {self.first_number}, {self.second_number} - Amount: {self.amount}"

class LotteryResult(models.Model):
    result_numbers = models.CharField(max_length=255)
    result_time = models.DateTimeField()

    def __str__(self):
        return f"Lottery Result - {self.result_time}"