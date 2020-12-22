from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.db import transaction
from .models import User, Customer
import random

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_customer = True
        user.save()

        # creating the customer object
        customer = Customer.objects.create(user=user)

        # random account number between 2000000 and 3000000 which only persists
        # if the account number doesn't exists in the database
        account_num = random.randint(2000000, 3000000)
        while(Customer.objects.filter(account_num=account_num).exists()):
            account_num = random.randint(2000000, 3000000)
        customer.account_num = account_num
        # preset account number
        customer.sort_code = "42-04-20"
        customer.save()


class UserInputQrCodeForm(forms.Form):
    code = forms.IntegerField(max_value=999999)
