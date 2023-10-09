from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import ClearableFileInput
from .models import User
from django.core.exceptions import ValidationError

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True)
    age = forms.IntegerField()

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone', 'age', 'gender', 'password1', 'password2']

    def save_user(self):
        user = super().save(commit=False)
        user.save()
        return user

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age is not None and age < 18:
            raise ValidationError("You must be at least 18 years old to sign up.")
        return age


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)


    
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User  
        fields = ['first_name', 'last_name', 'gender', 'phone', 'address', 'age', 'image', 'bank_name', 'account_number', 'account_name']

class WithdrawForm(forms.Form):
    amount = forms.FloatField(label='Withdrawal Amount (NGN)', min_value=5000)