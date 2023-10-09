from django.urls import path
from . import views
# from . views import adjust_balances_for_pending_wins

urlpatterns = [
    path('purchase_ticket/', views.purchase_ticket, name='play_lottery'),
    # path('adjust_balances_for_pending_wins/', views.adjust_balances_for_pending_wins, name='adjust_balances_for_pending_wins'),
    path('ticket_history/', views.ticket_history, name='lottery_history'),
    
    
    path('least_drawn_numbers/', views.least_drawn_numbers, name='least_drawn_numbers'),
    path('number_detail/<int:number>/', views.number_detail, name='number_detail'),
    # Add more URL patterns for other views as needed
]