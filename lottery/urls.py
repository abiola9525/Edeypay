from django.urls import path
from . import views

urlpatterns = [
    # path('play/', views1.play_lottery, name='play-lottery'),
    # path('results/', views1.lottery_results, name='lottery-results'),
    path('play/', views.play_lottery, name='purchase_ticket'),
    path('generate_result/', views.generate_lottery_result, name='generate_lottery_result'),
    path('history/', views.lottery_history, name='ticket_history'),
]