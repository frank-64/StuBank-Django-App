from django.shortcuts import render
from django.views import View
from dashboard.models import *


# Create your views here.
class FakeTransactions(View):

    def AddNewTransaction(request):
        t = Transaction
        return render(request, 'FakeTransactions/transactionPage.html')
