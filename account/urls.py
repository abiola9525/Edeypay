from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('payment-history/', views.payment_history, name='payment_history'),
    path('withdraw/', views.withdraw, name='withdraw'),
    path('initiate-payment/', views.initiate_payment, name='initiate-payment'),
    path('payment-verify/', views.verify_payment, name='payment-verify'),
    path('payment-failed/', views.payment_failed, name='payment-failed'),
    # path('deposit/', views.deposit_funds_view, name='deposit_funds'),
    # path('payment-success/', views.payment_success_view, name='payment_success'),
]
