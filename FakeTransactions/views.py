from django.shortcuts import render
from django.views import View


# Create your views here.
class FakeTransactions(View):

    def AddNewTransaction(request):
        return render(request, 'FakeTransactions/transactionPage.html')
