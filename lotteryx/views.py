from collections import Counter
from datetime import date, datetime, timezone
from django.db.models import Q
from django import forms
from django.shortcuts import get_object_or_404, redirect, render
from .models import LotteryTicket, LotteryDraw
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from django.utils import timezone as tz
from django.utils import timezone

def is_ticket_winner(ticket_id):
    try:
        ticket = LotteryTicket.objects.get(pk=ticket_id)
    except LotteryTicket.DoesNotExist:
        return "Ticket not found"
    print("Hi")
    current_winning_numbers = ticket.draw.winning_numbers.split(',')
    selected_numbers_list = ticket.selected_numbers.split(',')

    # Check if all winning numbers are zeros
    if all(number == '0' for number in current_winning_numbers):
        if ticket.is_winner != "Pending":  # Check if the ticket was not already pending
            ticket.is_winner = "Pending"
            ticket.save()
        return "Pending"

    if any(number in current_winning_numbers for number in selected_numbers_list):
        if ticket.is_winner == "Pending":  # Check if the ticket was pending and now becomes a winner
            # Calculate the winnings for this ticket
            amount_played = int(ticket.amount_played)
            prize_amount = int(amount_played * 20)  # Adjust this calculation as needed

            # Add winnings to the user's account balance for this ticket only
            ticket.user.account_balance += prize_amount
            ticket.user.save()
            print(ticket.amount_played)
            print(prize_amount)
            # Update the ticket's `is_winner` field to `Win`
            ticket.is_winner = "Win"
            ticket.save()
        return "Win"

    if ticket.is_winner != "Lose":  # Check if the ticket was not already a loser
        ticket.is_winner = "Lose"
        ticket.save()
    return "Lose"








# def is_ticket_winner(ticket_id):
#     # Get the lottery ticket with the specified ID
    
#     try:
#         ticket = LotteryTicket.objects.get(pk=ticket_id)
#     except LotteryTicket.DoesNotExist:
#         return False  # Ticket not found
#     print("Hello")
#     # Check if the ticket is pending.
#     if ticket.is_winner == "Pending":
#         # Check if the ticket is a winner by comparing the selected numbers to the winning numbers.
#         is_winner = is_ticket_winner(ticket)

#         if is_winner:
#             # Calculate the winnings and add them to the user's account balance.
#             winnings = int(ticket.amount_played * 2)
#             ticket.user.account_balance += winnings
#             ticket.user.save()

#             # Update the ticket's `is_winner` field to `Win`.
#             ticket.is_winner = "Win"
#             ticket.save()
        

    
#     # Get the latest draw associated with the ticket
#     latest_draw = LotteryDraw.objects.latest('draw_date')

#     # Get the winning numbers for the latest draw
#     winning_numbers = latest_draw.winning_numbers.split(',')  # Assuming winning numbers are stored as comma-separated values

#     # Split the selected numbers from the ticket
#     selected_numbers = ticket.selected_numbers.split(',')

#     # Check if any of the selected numbers match the winning numbers
#     for number in selected_numbers:
#         if number in winning_numbers:
#             # At least one match, so the ticket is a winner
#             return True

#     # No matches, so the ticket is not a winner
#     return False

# def is_ticket_winner(ticket):
#     current_winning_numbers = ticket.draw.winning_numbers.split(',')
#     selected_numbers_list = ticket.selected_numbers.split(',')

#     # Check if all winning numbers are zeros
#     if all(number == '0' for number in current_winning_numbers):
#         return "Pending"

#     # Check if any of the selected numbers match the winning numbers
#     if any(number in current_winning_numbers for number in selected_numbers_list):
#         if ticket.is_winner == "Pending":
#         # Calculate the winnings and add them to the user's account balance
#             winnings = int(ticket.amount_played * 2)  # Adjust this calculation as needed
#             ticket.user.account_balance += winnings
#             ticket.user.save()

#             # Update the ticket's `is_winner` field to `Win`
#             ticket.is_winner = "Win"
#             ticket.save()
#         return "Win"

#     # If none of the selected numbers match the winning numbers, the ticket is a loser
#     ticket.is_winner = "Lose"
#     ticket.save()
#     return "Lose"




def go(request):
    pass

@login_required
class PurchaseTicketForm(forms.Form):
    number1 = forms.CharField(max_length=255, required=True)
    number2 = forms.CharField(max_length=255, required=True)
    draw_id = forms.IntegerField()
    amount_played = forms.IntegerField(min_value=200, required=True)

# def purchase_ticket(request):
#     today = date.today()

#     if request.method == 'POST':
#         form = PurchaseTicketForm(request.POST)

#         if form.is_valid():
#             number1 = form.cleaned_data['number1']
#             number2 = form.cleaned_data['number2']
#             draw_id = form.cleaned_data['draw_id']
#             amount_played = form.cleaned_data['amount_played']

#             # Check if the user has a sufficient balance
#             user = request.user
#             if user.account_balance < amount_played:
#                 messages.error(request, "Insufficient balance.")
#                 return redirect('lottery:purchase_ticket')

#             # Deduct the amount from the user's account balance
#             user.account_balance -= amount_played
#             user.save()

#             # Create a new lottery ticket
#             draw = LotteryDraw.objects.get(pk=draw_id)
#             selected_numbers = f"{number1},{number2}"
#             ticket = LotteryTicket(user=user, selected_numbers=selected_numbers, draw=draw, amount_played=amount_played)
#             ticket.save()

#             # Check if the ticket is a winner based on the current winning numbers
#             ticket.is_winner = is_ticket_winner(ticket)
#             ticket.save()

#             # Handle balance adjustments
#             if ticket.is_winner:
#                 # user.account_balance += (amount_played * 2)  # Add winnings (assuming a fixed prize)
#                 user.save()
#                 messages.success(request, "Congratulations! You won.")
#             else:
#                 messages.info(request, "Sorry, you didn't win this time.")

#             return redirect('home')
#     else:
#         form = PurchaseTicketForm()

#     # Filter the draws to get only the draws for the current day
#     draws = LotteryDraw.objects.filter(draw_date__date=today)

#     return render(request, 'lottery/purchase_ticket.html', {'draws': draws, 'form': form})


@login_required
def least_drawn_numbers(request):
    # Get the current date
    current_date = timezone.now().date()

    # Query the database to get the 10 least drawn numbers for each draw of the current day
    least_drawn = []
    draws = LotteryDraw.objects.filter(draw_date__date=current_date)
    
    for draw in draws:
        # Get all selected numbers for the current draw
        selected_numbers = (
            LotteryTicket.objects.filter(draw=draw)
            .values_list('selected_numbers', flat=True)
        )
        
        # Split and flatten the selected numbers into individual numbers
        all_numbers = [int(number) for numbers in selected_numbers for number in numbers.split(',')]

        # Count the occurrences of each number
        number_counts = Counter(all_numbers)

        # Get the 10 least-selected numbers for this draw
        least_drawn_for_draw = number_counts.most_common()[:-11:-1]
        
        least_drawn.append((draw, least_drawn_for_draw))
    
    return render(request, 'lottery/least_drawn_numbers.html', {'least_drawn': least_drawn})


def number_detail(request, number):
    # Get the current date
    current_date = timezone.now().date()

    # Filter tickets for the given number and current day
    tickets_for_number = LotteryTicket.objects.filter(
        selected_numbers__contains=number,
        purchase_date__date=current_date
    )

    return render(request, 'lottery/number_detail.html', {'number': number, 'tickets_for_number': tickets_for_number})

@login_required
def purchase_ticket(request):
    current_datetime = datetime.now()
    today = current_datetime.date()
    # current_time = current_datetime.time()
    current_time = tz.now()

    if request.method == 'POST':
        form = PurchaseTicketForm(request.POST)

        if form.is_valid():
            number1 = form.cleaned_data['number1']
            number2 = form.cleaned_data['number2']
            draw_id = form.cleaned_data['draw_id']
            amount_played = form.cleaned_data['amount_played']

            # Check if the user has a sufficient balance
            user = request.user
            if user.account_balance < amount_played:
                messages.error(request, "Insufficient balance.")
                return redirect('lottery:purchase_ticket')

            # Check if the draw is open for ticket purchases based on the server's time
            
            
            # Deduct the amount from the user's account balance
            user.account_balance -= amount_played
            user.save()

            # Create a new lottery ticket
            draw = LotteryDraw.objects.get(pk=draw_id)
            selected_numbers = f"{number1},{number2}"
            ticket = LotteryTicket(user=user, selected_numbers=selected_numbers, draw=draw, amount_played=amount_played)
            ticket.save()

            # # Check if the ticket is a winner based on the current winning numbers
            # ticket.is_winner = is_ticket_winner(ticket)
            # ticket.save()

            # Handle balance adjustments if the ticket is a winner
            # if ticket.is_winner == "Win":
            #     user.account_balance += (amount_played * 2)  # Add winnings (assuming a fixed prize)
            #     user.save()
            #     messages.success(request, "Congratulations! You won.")
            # else:
            #     messages.info(request, "Sorry, you didn't win this time.")

            return render(request, 'lottery/purchase_success.html', {'ticket': ticket})
    else:
        form = PurchaseTicketForm()

    # Filter the draws to get only the draws for the current day
    draws = LotteryDraw.objects.filter(
        Q(draw_date__date=today, name__time__gt=current_time) | Q(draw_date__date__gt=today)
    )

    return render(request, 'lottery/purchase_ticket.html', {'draws': draws, 'form': form})






# def purchase_ticket(request):
#     if request.method == 'POST':
#         number1 = request.POST['number1']
#         number2 = request.POST['number2']
#         draw_id = request.POST['draw_id']
#         amount_played = float(request.POST['amount_played'])  # Convert to a float
#         draw = LotteryDraw.objects.get(pk=draw_id)
#         selected_numbers = f"{number1},{number2}"
        
#         # Check if the user has a sufficient balance
#         user = request.user
#         if user.account_balance < amount_played:
#             messages.error(request, "Insufficient balance.")
#             return redirect('lottery:purchase_ticket')
        
#         # Deduct the amount from the user's account balance
#         user.account_balance -= amount_played
#         user.save()
        
#         # Create a new lottery ticket
#         ticket = LotteryTicket(user=user, selected_numbers=selected_numbers, draw=draw, amount_played=amount_played)
#         ticket.save()

#         # Check if the ticket is a winner based on the current winning numbers
#         ticket.is_winner = is_ticket_winner(ticket)
#         ticket.save()

#         # Handle balance adjustments
#         if ticket.is_winner:
#             # user.account_balance += (amount_played * 2)  # Add winnings (assuming a fixed prize)
#             user.save()
#             messages.success(request, "Congratulations! You won.")
#         else:
#             messages.info(request, "Sorry, you didn't win this time.")
        
#         return redirect('home')

#     draws = LotteryDraw.objects.all()
    
#     return render(request, 'lottery/purchase_ticket.html', {'draws': draws})

# def ticket_history(request):
#     # Retrieve the user's lottery ticket history
#     ticket_history = LotteryTicket.objects.filter(user=request.user)
    
#     # Define a function to determine the winnings for each ticket
#     def get_winnings(ticket):
#         if not ticket.is_winner:
#             return "Lose"
#         winning_numbers = ticket.draw.winning_numbers.split(',')
#         selected_numbers = ticket.selected_numbers.split(',')
        
#         # Check if all winning numbers are zeros
#         if all(number == '0' for number in winning_numbers):
#             return "Pending"
        
#         if any(number in winning_numbers for number in selected_numbers):
#             return "Win"
#         return "Lose"
    
#     # Prepare data for the template
#     ticket_data = []
#     for ticket in ticket_history:
#         data = {
#             'name': ticket.draw.name,
#             'date': ticket.purchase_date,
#             'numbers_played': ticket.selected_numbers,
#             'amount_played': ticket.amount_played,  # Replace with the actual ticket price
#             'winning_numbers': ticket.draw.winning_numbers,
#             'winnings': get_winnings(ticket),
#         }
#         ticket_data.append(data)
    
#     return render(request, 'lottery/ticket_history.html', {'ticket_data': ticket_data})

# def ticket_history(request):
#     # Retrieve the user's lottery ticket history
#     ticket_history = LotteryTicket.objects.filter(user=request.user)
    
#     # Prepare data for the template
#     ticket_data = []
#     for ticket in ticket_history:
#         # Calculate winnings for the current ticket
#         is_winner = is_ticket_winner(ticket)
        
#         data = {
#             'name': ticket.draw.name,
#             'date': ticket.purchase_date,
#             'numbers_played': ticket.selected_numbers,
#             'amount_played': ticket.amount_played,
#             'winning_numbers': ticket.draw.winning_numbers,
#             'winnings': is_winner,  # Use the calculated winnings directly
#         }
#         ticket_data.append(data)
    
#     return render(request, 'lottery/ticket_history.html', {'ticket_data': ticket_data})

@login_required
def ticket_history(request):
    # Retrieve the user's lottery ticket history
    ticket_history = LotteryTicket.objects.filter(user=request.user)
    
    # Prepare data for the template
    ticket_data = []
    for ticket in ticket_history:
        # Calculate winnings for the current ticket using ticket_id
        is_winner = is_ticket_winner(ticket.id)
        
        data = {
            'name': ticket.draw.name,
            'date': ticket.purchase_date,
            'numbers_played': ticket.selected_numbers,
            'amount_played': ticket.amount_played,
            'winning_numbers': ticket.draw.winning_numbers,
            'winnings': is_winner,
        }
        ticket_data.append(data)
    
    return render(request, 'lottery/ticket_history.html', {'ticket_data': ticket_data})