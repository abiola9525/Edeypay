from random import sample
import random
from celery import Celery
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from .models import LotteryEntry, LotteryResult

# Create a Celery instance
app = Celery('lottery')




def play_lottery(request):
    if request.method == 'POST':
        user = request.user
        first_number = int(request.POST['first_number'])
        second_number = int(request.POST['second_number'])
        amount = float(request.POST['amount'])

        # Check if the user has enough balance to play
        if user.account_balance >= 200 and user.account_balance >= amount:
            # Create a new lottery entry
            lottery_entry = LotteryEntry(user=user, first_number=first_number, second_number=second_number, amount=amount)
            lottery_entry.save()

            # Deduct the amount from the user's account balance
            user.account_balance -= amount
            user.save()

            messages.success(request, 'You have successfully played the lottery!')
        else:
            messages.error(request, 'Insufficient balance to play the lottery.')

    return render(request, 'lottery/play_lottery.html')

# Define a Celery task to generate the lottery result
@app.task
def generate_lottery_result():
    """Generates the lottery result for the next time slot."""

    current_time = timezone.now()
    result_time = None

    # Determine the next time slot for the lottery result
    if current_time.hour < 8:
        result_time = timezone.make_aware(timezone.datetime(current_time.year, current_time.month, current_time.day, 8))
    elif current_time.hour < 11:
        result_time = timezone.make_aware(timezone.datetime(current_time.year, current_time.month, current_time.day, 11))
    elif current_time.hour < 14:
        result_time = timezone.make_aware(timezone.datetime(current_time.year, current_time.month, current_time.day, 14))
    elif current_time.hour < 17:
        result_time = timezone.make_aware(timezone.datetime(current_time.year, current_time.month, current_time.day, 17))
    elif current_time.hour < 20:
        result_time = timezone.make_aware(timezone.datetime(current_time.year, current_time.month, current_time.day, 20))

    if result_time:
        # Retrieve all user entries
        all_entries = LotteryEntry.objects.all()
        user_numbers = [entry.first_number for entry in all_entries] + [entry.second_number for entry in all_entries]

        # Ensure there are enough user numbers to sample from
        if len(user_numbers) >= 5:
            result_numbers = ' '.join(map(str, random.sample(set(user_numbers), 5)))
        else:
            # If there are not enough user numbers, generate random numbers
            result_numbers = ' '.join(map(str, random.sample(range(1, 78), 5)))

        # Create a new lottery result
        lottery_result = LotteryResult(result_numbers=result_numbers, result_time=result_time)
        lottery_result.save()

        # Check if any user has won and update their account balance
        for entry in all_entries:
            if str(entry.first_number) in result_numbers or str(entry.second_number) in result_numbers:
                # User has won
                entry.user.account_balance += entry.amount * 20
                entry.user.save()

    # Schedule the next lottery result generation
    generate_lottery_result.apply_async(eta=result_time + timezone.timedelta(days=1))

def lottery_history(request):
    # Retrieve the user's lottery entries and results
    user = request.user
      # Perform the multiplication in Python

    lottery_entries = LotteryEntry.objects.filter(user=user).order_by('-timestamp')
    for entry in lottery_entries:
        entry.potential_winnings = entry.amount * 20
    context = {
        'lottery_entries': lottery_entries,
        # 'potential_winnings': potential_winnings,
    }
    
    return render(request, 'lottery/lottery_history.html', context)
