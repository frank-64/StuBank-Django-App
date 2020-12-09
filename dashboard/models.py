from django.db import models

class Customer(models.Model):
    FirstName = models.CharField(max_length=20)
    LastName = models.CharField(max_length=20)
    SortCode = models.IntegerField(blank=False)
    AccountNumber = models.IntegerField(blank=False)
    # customer gets £100 upon account creation
    Balance = models.DecimalField(default=100, decimal_places=2, max_digits=10)
    # is the customer's account frozen?
    AccountFrozen = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id} {self.FirstName} {self.LastName} {self.SortCode} {self.AccountNumber} {self.Balance}"


class Payee(models.Model):
    # customerID that added the payee
    Customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    FirstName = models.CharField(max_length=20, blank=False)
    LastName = models.CharField(max_length=20, blank=False)
    SortCode = models.IntegerField(blank=False)
    AccountNumber = models.IntegerField(blank=False)

class Card(models.Model):
    Customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    CardFrozen = models.BooleanField(default=False)
    CardNum = models.IntegerField(blank=False)
    ExpiryDate = models.DateTimeField(blank=False)
    CVC = models.IntegerField(blank=False)

class Transaction(models.Model):
    class PurchaseCategory(models.TextChoices):
        FOOD = 'Food'
        CLOTHING = 'Clothing'
        PAYEE = 'Payee Transfer'
        OTHER = 'Other'
    # optional foreign key used to link payees to a transaction if transferring or receiving money from a payee
    Payee = models.ForeignKey(Payee, blank=True, null=True, on_delete=models.PROTECT)
    # this customer foreign key is used to relate a transaction to a customer
    Customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    # amount of the transaction
    Amount = models.DecimalField(blank=False,decimal_places=2, max_digits=10)
    # transaction in or out 1=in, 0=out
    Direction = models.BooleanField(blank=False, default=0)
    # this is the datetime the model object was created
    DateTime = models.DateTimeField(blank=False, editable=False)
    # any other comments with the transaction
    Comment = models.CharField(blank=True, max_length=200)
    # customer balance after transaction
    NewBalance = models.DecimalField(blank=False, decimal_places=2, max_digits=10)
    # name of payee or establishment e.g. McDonalds or Tesco
    Destination = models.CharField(blank=False, max_length=50)
    # this attribute will be used the machine learning to determine probability of certain categories
    Category = models.CharField(blank=False, choices=PurchaseCategory.choices, default=PurchaseCategory.OTHER, max_length=20)
