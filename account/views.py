from django.shortcuts import render, redirect
from django.views import View
from django.utils import timezone
from datetime import datetime
import uuid
from django.contrib.auth import login, authenticate
from .forms import SignupForm, LoginForm, WithdrawForm
from . models import User, PaymentTransaction, Withdraw
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
# from .paystack import initiate_payment, verify_payment
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import PaymentTransaction
import requests
import json


def home(request):
    count = User.objects.count()
    return render(request, 'home.html', {
        'count': count
    })

@login_required
def payment_history(request):
    user = request.user
    historys = PaymentTransaction.objects.filter(user=user).order_by('-timestamp')
    withdrawals = Withdraw.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'payment_history.html', {
        'historys':historys,
        'withdrawals': withdrawals,
    })

# def about(request):
#     return render(request, 'about.html')

# def contact(request):
#     return render(request, 'contact.html')

# def service(request):
#     return render(request, 'services.html')

class SignupView(View):
    def get(self, request):
        form = SignupForm()
        return render(request, 'registration/signup.html', {'form': form})

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save_user()
            login(request, user)
            return redirect('home')  # Redirect to the home page


PAYSTACK_SECRET_KEY = settings.PAYSTACK_SECRET_KEY

def initiate_payment(request):
    if request.method == 'POST':
        user = request.user
        amount = request.POST['amount']
        email = request.user.email
        
        redirect_url = request.build_absolute_uri(reverse('payment-verify'))

        initialize_url = 'https://api.paystack.co/transaction/initialize'
        headers = {
            'Authorization': f'Bearer {PAYSTACK_SECRET_KEY}',
            'Content-Type': 'application/json',
        }
        data = {
            'amount': int(amount) * 100,  # Amount in kobo (1 Naira = 100 kobo)
            'email': email,
            'reference': f"user_{user.id}_{uuid.uuid4().hex}_payment",
            'callback_url': redirect_url,  # URL to handle payment verification
        }

        response = requests.post(initialize_url, headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            response_data = response.json()
            authorization_url = response_data['data']['authorization_url']
            return HttpResponseRedirect(authorization_url)

    messages.error(request, 'Payment initiation failed.')
    return render(request, 'payment.html')

def verify_payment(request):
    reference = request.GET.get('reference')

    verify_url = f'https://api.paystack.co/transaction/verify/{reference}'
    headers = {
        'Authorization': f'Bearer {PAYSTACK_SECRET_KEY}',
    }

    response = requests.get(verify_url, headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        if response_data.get('status'):
            # Payment is successful
            transaction = PaymentTransaction.objects.create(
                user=request.user,
                amount=float(response_data['data']['amount']) / 100,  # Convert from kobo to Naira
                reference=reference,
                status=True
            )
            
            user = request.user
            amount = transaction.amount
            user.account_balance += amount
            user.save()
            return render(request, 'payment_success.html', {'transaction': transaction})

    messages.error(request, 'Payment verification failed.')
    return redirect('payment-failed')

def payment_failed(request):
    return render(request, 'payment_failed.html')


def withdraw(request):
    if request.method == 'POST':
        form = WithdrawForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            user = request.user

            if user.account_balance < amount:
                # Insufficient funds
                messages.error(request, 'Insufficient funds for withdrawal.')
            elif amount < 5000:
                # Withdrawal amount less than 5000
                messages.error(request, 'Withdrawal amount must be at least 5000 NGN.')
            else:
                # Withdrawal is successful
                user.account_balance -= amount
                user.save()
                Withdraw.objects.create(user=user, amount=amount, status=False)
                messages.success(request, 'Withdrawal successful.')
                return redirect('payment_history')  # Redirect to withdrawal history page

    else:
        form = WithdrawForm()

    return render(request, 'withdraw.html', {'form': form})






# @login_required
# def deposit_funds_view(request):
#     if request.method == 'POST':
#         amount = float(request.POST.get('amount', 0))
#         email = request.user.email

#         if amount < 200:
#             messages.error(request, 'Minimum deposit amount is 200 Naira.')
#             return redirect('deposit_funds')

#         payment_response = initiate_payment(request, amount, email)

#         if payment_response:
#             return payment_response
#         else:
#             messages.error(request, 'Payment initiation failed.')
#             return redirect('deposit_funds')

#     return render(request, 'deposit_funds.html')

# @login_required
# def payment_success_view(request):
#     reference = request.GET.get('reference')

#     if reference and verify_payment(reference):
#         # Payment verification is successful, update the user's account balance
#         user = request.user
#         amount = float(request.GET.get('amount', 0))
#         user.account_balance += amount
#         user.save()

#         # Create a transaction record in the database
#         PaymentTransaction.objects.create(
#             user=user,
#             amount=amount,
#             reference=reference
#         )
        
#         messages.success(request, f'Payment of {amount} Naira successful. Your new account balance is {user.account_balance} Naira.')
#         return render(request, 'payment_success.html', {'user': user, 'transaction': amount})
    
#     messages.error(request, 'Payment verification failed.')
#     return HttpResponseRedirect(reverse('deposit_funds'))