from django import forms
from django.db import transaction
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import User, Customer, Management, Admin

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    # Specifiy what we went this form to interact with:
    class Meta:
        # The model that will be affected is the user model
        model = User
        # And these fields are the fields we want in the form and in what order
        fields = ['username', 'email', 'password1', 'password2']

    @transaction.atomic # Makes sure these operations are done in a single database transaction
    def save(self):
        user = super().save(commit=False)
        user.is_customer = True
        user.save()
        #customer.account_num.add(1236271)
        return user