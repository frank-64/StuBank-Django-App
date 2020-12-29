from django.shortcuts import render
from django.views import View
from FakeTransactions.forms import FakeForm
from dashboard.models import *


# Create your views here.
class FakeTransactions(View):

    def AddNewTransaction(request):
        t = Transaction
        context = {}
        context['form'] = FakeForm()
        return render(request, 'FakeTransactions/transactionPage.html', context)
