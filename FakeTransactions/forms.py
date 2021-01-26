from django import forms

from dashboard.models import Transaction, Card


class StuShopForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(StuShopForm, self).__init__(*args, **kwargs)
        try:
            self.fields['Card'].queryset = Card.objects.filter(Customer_id=user.pk)
        except Card.DoesNotExist:
            pass
    class Meta:
        model = Transaction
        exclude = ['Direction', 'TransactionTime', 'NewBalance', 'Customer', 'Method', 'Payee']
