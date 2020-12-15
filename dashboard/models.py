from django.db import models
from django.utils import timezone

from accounts.models import *

class Payee(models.Model):
    # customerID that added the payee
    Customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    FirstName = models.CharField(max_length=20, blank=False)
    LastName = models.CharField(max_length=20, blank=False)
    SortCode = models.IntegerField(blank=False)
    AccountNumber = models.IntegerField(blank=False)

    def __str__(self):
        return f"ID:{self.id}, Username:{self.Customer.user.username}"

class Card(models.Model):
    Customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    CardFrozen = models.BooleanField(default=False)
    CardNum = models.BigIntegerField(blank=False)
    ExpiryDate = models.DateField(blank=False)
    CVC = models.IntegerField(blank=False)

    def __str__(self):
        return f"ID:{self.id}, Username:{self.Customer.user.username}"


class Transaction(models.Model):
    CATEGORY = (
        ('Food', 'Food'),
        ('Transportation', 'Transportation'),
        ('Drink', 'Drink'),
        ('Entertainment', 'Entertainment'),
        ('Technology', 'Technology'),
        ('Clothing', 'Clothing'),
        ('ATM Withdrawal', 'ATM Withdrawal'),
        ('ATM Deposit', 'ATM Deposit'),
        ('Cheque Deposit', 'Cheque Deposit'),
        ('Bank Transfer', 'Bank Transfer')
    )
    class Direction(models.TextChoices):
        IN = 'In'
        OUT = 'Out'
    # optional foreign key used to link payees to a transaction if transferring or receiving money from a payee
    Payee = models.ForeignKey(Payee, blank=True, null=True, on_delete=models.PROTECT)
    # this customer foreign key is used to relate a transaction to a customer
    Customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    # direction of the transfer e.g. payment into account or transaction out of account
    Amount = models.DecimalField(blank=False,decimal_places=2, max_digits=10)
    # transaction direction e.g. is money being removed from the account or added
    Direction = models.CharField(blank=False, choices=Direction.choices, default=Direction.OUT, max_length=10)
    # this is the datetime the model object was created
    TransactionTime = models.CharField(blank=False, max_length=50, default=timezone.now())
    # any other comments with the transaction
    Comment = models.CharField(blank=True, max_length=200)
    # customer balance after transaction
    NewBalance = models.DecimalField(blank=False, decimal_places=2, max_digits=10)
    # name of payee or establishment e.g. McDonalds or Tesco
    Destination = models.CharField(blank=False, max_length=50)
    # this attribute will be used the machine learning to determine probability of certain categories
    Category = models.CharField(blank=False, choices=CATEGORY, max_length=20)

    def __str__(self):
        return f"ID:{self.id}, Username:{self.Customer.user.username}"
