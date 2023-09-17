# account/middleware.py

from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from .models import CustomUser
from .paystack import initiate_payment, verify_payment

class AccountBalanceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            user = request.user
            if request.method == 'POST':
                # Check if 'amount' is in the POST data
                amount = float(request.POST.get('amount', 0))
                if amount < 200:
                    messages.error(request, 'Minimum deposit amount is 200 Naira.')
                    return redirect(reverse('deposit_funds'))

                payment_data = initiate_payment(amount)

                if not payment_data:
                    messages.error(request, 'Payment initiation failed.')
                    return redirect(reverse('deposit_funds'))

                # In a real application, redirect to the actual Paystack payment page here
                # Example: return redirect(payment_data['authorization_url'])

                reference = request.GET.get('reference')
                if reference and verify_payment(reference):
                    user.account_balance += amount
                    user.save()
                    messages.success(request, f'Payment of {amount} Naira successful. Your new account balance is {user.account_balance} Naira.')
                else:
                    messages.error(request, 'Payment verification failed.')

                return redirect(reverse('account_balance'))

        response = self.get_response(request)
        return response
