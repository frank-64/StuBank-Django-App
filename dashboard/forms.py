from django import forms
from dashboard.models import *


class PayeeDetailsForm(forms.Form):
    """
        Written by: Frankie
        Purpose:
    """

    first_name = forms.CharField(required=True, max_length=20)
    last_name = forms.CharField(required=True, max_length=20)
    sort_code = forms.CharField(required=True, max_length=20)
    account_num = forms.IntegerField(required=True)


class TransferForm(forms.ModelForm):
    """
        Written by: Frankie and Ed
        Purpose:
    """

    pot = forms.ModelChoiceField(queryset=MoneyPot.objects.none())

    class Meta:
        model = Transaction
        fields = ['Payee', 'Amount', 'Comment', 'Category']

    def __init__(self, user, *args, **kwargs):
        super(TransferForm, self).__init__(*args, **kwargs)
        try:
            customer = Customer.objects.get(user=user)
            pots = MoneyPot.objects.filter(customer_id=customer.pk)
            self.fields['pot'].queryset = pots
            self.fields['Payee'].queryset = Payee.objects.filter(User_id=user.pk)
        except Payee.DoesNotExist:
            pass


class CardTransaction(forms.ModelForm):
    """
        Written by: Frankie
        Purpose:
    """
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


class DepositForm(forms.Form):
    """
        Written by: Frankie
        Purpose:
    """

    amount = forms.DecimalField(required=True, decimal_places=2, max_digits=10)
