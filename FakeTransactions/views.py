from django.http import *
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import View
from dashboard.models import *
from decimal import Decimal
import json
from dashboard.views import *

# Create your views here.


# Runs results from the StuShop page to the transaction method
@csrf_exempt
def AddNewTransaction(request):
    if request.method == "POST":

        transaction_variables = request.body.decode('UTF-8')
        # Loads as json Object
        json_details = json.loads(transaction_variables)
        # Gets customer ID
        customer_id = request.user.pk
        # Gets Card details
        card = get_object_or_404(Card, Customer_id=request.user.pk)

        transaction_time = timezone.now()
        # Gets variables from json
        comment = json_details['comment']

        amount = Decimal(json_details['amount'])

        termini = json_details['termini']

        category = json_details['category']

        new_balance = get_new_balances(customer_id, -1, amount)

        method = 'Card Transaction'
        # Sends data to transaction method
        card_transaction_object = Transaction(Card_id=card.pk, Customer_id=customer_id,
                                              Amount=amount,
                                              Direction='Out', TransactionTime=transaction_time, Comment=comment,
                                              NewBalance=new_balance[0], Termini=termini, Category=category,
                                              Method=method)
        try:
            card_transaction_object.save()
            alter_balance(customer_id, new_balance[0])
            return HttpResponse('Complete')
        except:
            return HttpResponse('Error')


# Renders page
def StuShopRender(request):
    return render(request, 'FakeTransactions/transactionPage.html')


