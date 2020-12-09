from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    # Specifiy what we went this form to interact with:
    class Meta:
        # The model that will be affected is the user model
        model = User
        # And these fields are the fields we want in the form and in what order
        fields = ['username', 'email', 'password1', 'password2']