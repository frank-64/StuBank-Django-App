from django.db import models


# Create your models here.

class Food(models.Model):
    FOODTYPES = (
        ('Fast Food', 'Fast Food'),
        ('Chinese', 'Chinese'),
        ('Groceries', 'Groceries'),
    )
    FoodType = models.CharField(max_length=20, blank=True, choices=FOODTYPES)
    price = models.FloatField(null=False)
    quantity = models.IntegerField(null=False)


class Clothes(models.Model):
    CLOTHESTYPES = (
        ('Shirt', 'Shirt'),
        ('Jeans', 'Jeans'),
        ('Shorts', 'Shorts'),
    )

    ClothesType = models.CharField(max_length=20, blank=True, choices=CLOTHESTYPES)
    price = models.FloatField(null=False)
    quantity = models.IntegerField(null=False)


class Drink(models.Model):
    DRINKTYPES = (
        ('Alcohol', 'Alcohol'),
        ('Fizzy Drink', 'Fizzy Drink'),
        ('Water', 'Water'),
    )
    DrinkType = models.CharField(max_length=20, blank=True)
    price = models.FloatField(null=False)
    quantity = models.IntegerField(null=False)


class Payee(models.Model):
    PayeeID = models.CharField(max_length=20, blank=True)
    incoming = models.FloatField(null=False)
    PayeeDesc = models.CharField(max_length=20, blank=True)


class Cheque(models.Model):
    ChequeId = models.CharField(max_length=20, blank=True)
    incoming = models.FloatField(null=False)
    ChequeOwner = models.CharField(max_length=20, blank=True)
