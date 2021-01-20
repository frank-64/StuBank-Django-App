from decimal import Decimal

from django.core.validators import MinValueValidator
from django.utils import timezone

from accounts.models import *

class Payee(models.Model):
    """
        Written by: Frankie
        Purpose:
    """

    # customerID that added the payee
    User = models.ForeignKey(User, on_delete=models.PROTECT)
    PayeeID = models.ForeignKey(Customer, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.PayeeID.user.first_name} {self.PayeeID.user.last_name}: {self.PayeeID.sort_code} {self.PayeeID.account_num}"


class Card(models.Model):
    """
        Written by: Frankie
        Purpose:
    """

    Customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    CardFrozen = models.BooleanField(default=False)
    CardNum = models.BigIntegerField(blank=False, unique=True)
    MaskCardNum = models.CharField(blank=False, max_length=16, default='xxxxxxxxxxxxxxxx')
    ExpiryDate = models.DateField(blank=False)
    CVC = models.CharField(blank=False, max_length=3)

    def __str__(self):
        return f"{self.MaskCardNum}"


class Transaction(models.Model):
    """
        Written by: Frankie
        Purpose:
    """

    CATEGORY = (
        ('Dining Out', 'Dining Out'),
        ('Food Shopping', 'Food Shopping'),
        ('Transportation', 'Transportation'),
        ('Entertainment', 'Entertainment'),
        ('Technology', 'Technology'),
        ('Clothing', 'Clothing'),
        ('Rent', 'Rent'),
        ('Healthcare', 'Healthcare'),
        ('Other', 'Other'),
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
    # optional foreign key used to link the card used with the customer who made the transaction
    Card = models.ForeignKey(Card, blank=True, null=True, on_delete=models.PROTECT)
    # optional foreign key used to link payees to a transaction if transferring or receiving money from a payee
    Payee = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT)
    # this customer foreign key is used to relate a transaction to a customer
    Customer = models.ForeignKey(Customer, blank=True, null=True, on_delete=models.PROTECT)
    # direction of the transfer e.g. payment into account or transaction out of account
    Amount = models.DecimalField(blank=False, decimal_places=2, max_digits=10)
    # transaction direction e.g. is money being removed from the account or added
    Direction = models.CharField(blank=False, choices=Direction.choices, default=Direction.OUT, max_length=10)
    # time the transaction took place
    TransactionTime = models.DateTimeField(blank=False)
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


class MoneyPot(models.Model):
    """
        Written by: Ed
        Purpose:
    """

    def __str__(self):
        return str(self.name) + " - (£" + str(self.pot_balance) + ")"

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    name = models.CharField(blank=False, default='My Money Pot', max_length=100)
    target_balance = models.DecimalField(blank=False, decimal_places=2, max_digits=10, validators=[MinValueValidator
                                                                                                   (Decimal('0.01'))])
    pot_balance = models.DecimalField(blank=False, default=0, decimal_places=2, max_digits=10)


class Message(models.Model):
    """
        Written by: Frankie
        Purpose:
    """

    sender = models.ForeignKey(User, related_name='sent', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received', on_delete=models.CASCADE)
    seen = models.BooleanField(default=False)
    message = models.TextField()
    created_at = models.DateTimeField()

class LiveChat(models.Model):
    """
        Written by: Frankie
        Purpose:
    """

    customer = models.ForeignKey(User, related_name='customer_livechat', on_delete=models.CASCADE)
    helper = models.ForeignKey(User, related_name='helper_livechat', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    perm_granted = models.BooleanField(default=False)

    def __str__(self):
        return f"ID:{self.id}, Customer:{self.customer.username}, CustomerID:{self.helper.username}"