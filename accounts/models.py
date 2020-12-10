from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_helper = models.BooleanField(default=False)


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    account_num = models.IntegerField(null=True, blank=True)
    sort_code = models.CharField(null=True, blank=True, max_length=20)
    balance = models.IntegerField(null=True, blank=True)


class Helper(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
