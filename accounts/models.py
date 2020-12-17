import qrcode
from django.core.files.base import ContentFile
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_helper = models.BooleanField(default=False)

    def __str__(self):
        return f"ID:{self.id}, Username:{self.username}"


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    account_num = models.IntegerField(null=True, blank=True)
    sort_code = models.CharField(null=True, blank=False, max_length=20)
    balance = models.DecimalField(null=True, blank=False, max_digits=9, decimal_places=2, default=100)
    account_frozen = models.BooleanField(default=False, blank=False)
    qrcode_file = models.ImageField(upload_to='qr_codes', blank=True, null=True)
    qrcode_generated = models.BooleanField(default=False, blank=False)

    def __str__(self):
        return f"ID:{self.user.id}, Username:{self.user.username}"


class Helper(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return f"ID:{self.user.id}, Username:{self.user.username}"

