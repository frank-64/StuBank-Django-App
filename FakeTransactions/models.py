from django.db import models
from django.http import request


from FakeTransactions import costs


# Create your models here.
# Use checkboxes and costs.py to add up what user chose
def Food(request):
    groceriesCheck = request.POST['Groceries']
