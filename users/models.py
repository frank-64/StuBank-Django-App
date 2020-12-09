from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # One to one relationship with user model
    # Now a user is associated with this profile.

    #Return a string of the users username
    def __str__(self):
        return f'{self.user.username} Profile'