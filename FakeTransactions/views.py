from django.shortcuts import render
from django.views import View
from FakeTransactions.forms import *
from dashboard.models import *


# Create your views here.
class FakeTransactions(View):

    def AddNewTransaction(request):
        t = Transaction
        food_context = {'form': TransactionForm()}
        return render(request, 'FakeTransactions/transactionPage.html', food_context)
