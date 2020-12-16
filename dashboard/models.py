from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

from accounts.models import *

class Payee(models.Model):
    # customerID that added the payee
    User = models.ForeignKey(User, on_delete=models.PROTECT)
    PayeeID = models.ForeignKey(Customer, on_delete=models.PROTECT)

    def __str__(self):
        return f"Username: {self.PayeeID.user.username}, Name:{self.PayeeID.user.first_name} {self.PayeeID.user.last_name}"

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
        ('Bank Transfer', 'Bank Transfer'),
    )

    class Method(models.TextChoices):
        ATM_Withdrawal = 'ATM Withdrawal'
        ATM_Deposit = 'ATM Deposit'
        Cheque_Deposit = 'Cheque Deposit'
        Bank_Transfer = 'Bank Transfer'
        Card_Transaction = 'Card Transaction'

    class Direction(models.TextChoices):
        IN = 'In'
        OUT = 'Out'
    # optional foreign key used to link payees to a transaction if transferring or receiving money from a payee
    Payee = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT)
    # this customer foreign key is used to relate a transaction to a customer
    Customer = models.ForeignKey(Customer, blank=True, null=True, on_delete=models.PROTECT)
    # direction of the transfer e.g. payment into account or transaction out of account
    Amount = models.DecimalField(blank=False,decimal_places=2, max_digits=10, validators=[MinValueValidator(Decimal('1.00'))])
    # transaction direction e.g. is money being removed from the account or added
    Direction = models.CharField(blank=False, choices=Direction.choices, default=Direction.OUT, max_length=10)
    # this is the datetime the model object was created
    TransactionTime = models.CharField(blank=False, max_length=50)
    # any other comments with the transaction
    Comment = models.CharField(blank=True, max_length=200)
    # customer balance after transaction
    NewBalance = models.DecimalField(blank=False, decimal_places=2, max_digits=10)
    # This is the destination/origin of the transaction e.g.
    # If the transfer is IN then the termini would be the name of the person who transferred the money
    # If the transfer was OUT then the termini would be the name of the payee
    Termini = models.CharField(blank=False, max_length=50)
    # this attribute will be used the machine learning to determine probability of certain categories
    Category = models.CharField(blank=False, choices=CATEGORY, max_length=20)
    Method = models.CharField(blank=False, choices=Method.choices, max_length=20, default=Method.Bank_Transfer)

    def __str__(self):
        return f"ID:{self.id}, PayeeID:{self.Payee_id}, CustomerID:{self.Customer}"
