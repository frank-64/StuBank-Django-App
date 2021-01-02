from django import forms

TRANSACTION_CHOICES = (
    ('Food', (
        ("1", "Groceries"),
        ("2", "Fast Food"),
        ("3", "Snack"),
    )),
    ('Clothes', (
        ("1", "Jeans"),
        ("2", "Shorts"),
        ("3", "Shirt"),
    ))
)


class TransactionForm(forms.Form):
    Transactions = forms.ChoiceField(choices=TRANSACTION_CHOICES)
