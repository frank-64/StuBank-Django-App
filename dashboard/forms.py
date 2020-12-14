from django import forms

class PayeeDetails(forms.Form):
    first_name = forms.CharField(required=True, max_length=20)
    last_name = forms.CharField(required=True, max_length=20)
    account_num = forms.IntegerField(required=True)
    sort_code = forms.CharField(required=True, max_length=20)

