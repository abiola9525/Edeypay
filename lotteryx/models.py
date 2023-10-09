# models.py in 'lottery' app
from django.db import models
from account.models import User

class Game(models.Model):
    name = models.CharField(max_length=50)
    time = models.TimeField()
    
    def __str__(self):
        return f"{self.name} - {self.time}"

class LotteryDraw(models.Model):
    name = models.ForeignKey(Game, on_delete=models.CASCADE)
    draw_date = models.DateTimeField()
    winning_numbers = models.CharField(max_length=255, default='0,0,0,0,0')
    
    def __str__(self):
        return f"{self.name.name}"

class LotteryTicket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    selected_numbers = models.CharField(max_length=255)
    purchase_date = models.DateTimeField(auto_now_add=True)
    amount_played = models.CharField(max_length=50)
    draw = models.ForeignKey(LotteryDraw, on_delete=models.CASCADE)
    
    is_winner = models.CharField(max_length=10, choices=[("Pending", "Pending"), ("Win", "Win"), ("Lose", "Lose")], default="Pending")
    
    class Meta:
        ordering = ['-purchase_date']
    
    def __str__(self):
        return f"{self.draw.name.name} - {self.selected_numbers}({self.amount_played})"
