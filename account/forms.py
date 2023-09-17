from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone', 'address', 'gender', 'image', 'password1', 'password2']

    def save_user(self):
        user = super().save(commit=False)
        user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    

class WithdrawForm(forms.Form):
    amount = forms.FloatField(label='Withdrawal Amount (NGN)', min_value=5000)