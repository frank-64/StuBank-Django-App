from django import forms
from dashboard.models import *

class PayeeDetailsForm(forms.Form):
    first_name = forms.CharField(required=True, max_length=20)
    last_name = forms.CharField(required=True, max_length=20)
    sort_code = forms.CharField(required=True, max_length=20)
    account_num = forms.IntegerField(required=True)


class TransferForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(TransferForm, self).__init__(*args, **kwargs)
        try:
            self.fields['Payee'].queryset = Payee.objects.filter(User_id=user.pk)
        except Payee.DoesNotExist:
            ### there is not payee corresponding to this user
            pass
    class Meta:
        model = Transaction
        exclude = ['Direction', 'Termini', 'TransactionTime', 'NewBalance', 'Customer', 'Method', 'Card']

    #Payee = forms.ModelChoiceField(required=True, queryset=None, help_text="Who would you like to transfer to?")


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

    #Payee = forms.ModelChoiceField(required=True, queryset=None, help_text="Who would you like to transfer to?")


class DepositForm(forms.Form):
    amount = forms.DecimalField(required=True, decimal_places=2, max_digits=10)