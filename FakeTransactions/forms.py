from django import forms

from dashboard.models import Transaction, Card

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


class CardTransaction(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(CardTransaction, self).__init__(*args, **kwargs)
        try:
            self.fields['Card'].queryset = Card.objects.filter(Customer_id=user.pk)
        except Card.DoesNotExist:
            pass

    class Meta:
        model = Transaction
        exclude = ['Direction', 'TransactionTime', 'NewBalance', 'Customer', 'Method', 'Payee']

    # Payee = forms.ModelChoiceField(required=True, queryset=None, help_text="Who would you like to transfer to?")


class TransactionForm(forms.Form):
    Transactions = forms.ChoiceField(choices=TRANSACTION_CHOICES)
