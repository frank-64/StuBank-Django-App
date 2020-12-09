from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_management = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    account_num = models.IntegerField()
    sort_code = models.CharField(max_length=20)


class Management(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)


class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
