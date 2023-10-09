# from collections import Counter
# from django.contrib import messages
# from django.shortcuts import render, redirect
# from account.models import User 
# from .models import LotteryTicket
# from django.contrib.auth.decorators import login_required
# from .forms import LotteryPlayForm
# from datetime import time, timedelta, datetime
# from django.utils import timezone
# import random

# @login_required
# def play_lottery(request):
#     if request.method == 'POST':
#         form = LotteryPlayForm(request.POST)
#         if form.is_valid():
#             numbers = form.cleaned_data['numbers'].split(',')
#             amount_played = form.cleaned_data['amount_played']
#             user = request.user  # Access the currently logged-in user

#             if user.account_balance < amount_played:
#                 messages.error(request, 'Insufficient funds for playing the lottery.')
#             else:
#                 user.account_balance -= amount_played
#                 user.save()
#                 ticket = LotteryTicket.objects.create(user=user, numbers=numbers, amount_played=amount_played)
#                 messages.success(request, 'Lottery ticket purchased successfully.')

#                 # Schedule result generation
#                 result_time = get_result_time()
#                 ticket.result_time = result_time
#                 ticket.save()

#                 return redirect('lottery-results')

#     else:
#         form = LotteryPlayForm()

#     return render(request, 'lottery/play_lottery.html', {'form': form})

# def get_result_time():
#     now = timezone.now()
#     # Define the time slots for results
#     result_times = [time(8, 0), time(9, 20), time(14, 0), time(17, 0), time(20, 0)]

#     # Find the next result time that is greater than the current time
#     for result_time in result_times:
#         result_datetime = now.replace(hour=result_time.hour, minute=result_time.minute, second=0, microsecond=0)
#         if result_datetime > now:
#             return result_datetime

#     # If all result times are in the past, schedule the next result for 8 am the next day
#     next_day = now + timedelta(days=1)
#     return next_day.replace(hour=8, minute=0, second=0, microsecond=0)
    

# @login_required
# def lottery_results(request):
#     now = timezone.now()
#     tickets = LotteryTicket.objects.filter(result_time__lt=now, result__isnull=True)

#     if tickets:
#         for ticket in tickets:
#             # Generate lottery result
#             result = generate_lottery_result()
#             ticket.result = result
#             ticket.save()

#             # Check if the user won and credit winnings
#             if any(num in ticket.numbers for num in result):
#                 user = ticket.user
#                 user.account_balance += ticket.amount_played * 20
#                 user.save()

#     results = LotteryTicket.objects.filter(
#         user=request.user,
#         result_time__lt=now
#     ).order_by('-result_time')
    
#     next_result_time = get_result_time()
#     time_remaining = next_result_time - now
#     hours, remainder = divmod(time_remaining.seconds, 3600)
#     minutes, seconds = divmod(remainder, 60)

#     print("Now:", now)
#     print("Next Result Time:", next_result_time)
#     print("Hours Remaining:", hours)
#     print("Minutes Remaining:", minutes)
#     print("Seconds Remaining:", seconds)
    
#     return render(request, 'lottery/lottery_results.html', {
#         'results': results,
#         'next_result_time': next_result_time,
#         'hours_remaining': hours,
#         'minutes_remaining': minutes,
#         'seconds_remaining': seconds
#         })

# def generate_lottery_result():
#     all_numbers = [str(i) for i in range(1, 78)]
#     random.shuffle(all_numbers)

#     # Select the two least occurring numbers
#     count = Counter(all_numbers)
#     least_occurring = count.most_common()[:-3:-1]

#     result = [number for number, _ in least_occurring]
#     return result