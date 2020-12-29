from django import forms

FAKE_CHOICES = (
    ("1", "Groceries"),
    ("2", "FastFood")
)


class FakeForm(forms.Form):
    Transactions = forms.MultipleChoiceField(choices=FAKE_CHOICES)
