# # account/paystack.py

# from django.http import HttpResponseRedirect
# import requests
# import json
# from django.conf import settings
# from django.contrib import messages
# from . models import PaymentTransaction
# import logging

# logger = logging.getLogger(__name__) 

# PAYSTACK_SECRET_KEY = settings.PAYSTACK_SECRET_KEY  # Replace with your actual secret key

# def initiate_payment(request, amount, email):
#     initialize_url = 'https://api.paystack.co/transaction/initialize'
#     headers = {
#         'Authorization': f'Bearer {PAYSTACK_SECRET_KEY}',
#         'Content-Type': 'application/json',
#     }
#     data = {
#         'amount': int(amount) * 100,  # Amount in kobo (1 Naira = 100 kobo)
#         'email': email,  # Replace with the user's email
#         'redirect_url': request.build_absolute_uri('payment_success'),  # Redirect to a success page in your app
#     }

#     response = requests.post(initialize_url, headers=headers, data=json.dumps(data))

#     if response.status_code == 200:
#         response_data = response.json()
#         authorization_url = response_data['data']['authorization_url']
        
#         # Redirect the user to the Paystack payment page
#         return HttpResponseRedirect(authorization_url)
#     messages.error(request, 'Payment initiation failed.')
#     return None

# def verify_payment(reference):
#     verify_url = f'https://api.paystack.co/transaction/verify/{reference}'
#     headers = {
#         'Authorization': f'Bearer {PAYSTACK_SECRET_KEY}',
#     }

#     response = requests.get(verify_url, headers=headers)

#     try:
#         if response.status_code == 200:
#             response_data = response.json()
#             if response_data.get('status') == True:  # Check for successful status
#                 # Retrieve the associated transaction using the reference
#                 transaction = PaymentTransaction.objects.get(reference=reference)
#                 user = transaction.user
#                 amount = float(response_data['data']['amount']) / 100  # Convert from kobo to Naira

#                 # Update the user's account balance
#                 user.account_balance += amount
#                 user.save()

#                 # Update the transaction record in the database
#                 transaction.amount = amount
#                 transaction.status = True  # Set the status to True for a successful transaction
#                 transaction.save()

#                 return True

#         # If the transaction is not successful, update the status field to False
#         transaction = PaymentTransaction.objects.filter(reference=reference).first()
#         if transaction:
#             transaction.status = False
#             transaction.save()
        
#         logger.error(f"Payment verification failed for reference '{reference}'")

#     except PaymentTransaction.DoesNotExist:
#         logger.error(f"Transaction with reference '{reference}' not found in the database.")
#     except Exception as e:
#         logger.error(f"An error occurred while processing the payment: {str(e)}")

#     return False