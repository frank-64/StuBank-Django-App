from django.http import *
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import View
from FakeTransactions.forms import *
from FakeTransactions.models import Category, Product
from dashboard.models import *
from decimal import Decimal
import json
from dashboard.views import *


# Create your views here.

@csrf_exempt
def AddNewTransaction(request):
    if request.method == "POST":

        transaction_variables = request.body.decode('UTF-8')

        json_details = json.loads(transaction_variables)
        "apply the variables like this"

        """         try:
            payee_customer = Customer.objects.filter(sort_code=json_details['sort_code'],
                                                     account_num=json_details['account_num'],
                                                     user__first_name=json_details['firstname'],
                                                     user__last_name=json_details['lastname'])

            if payee_customer[0] == request.user.customer:
                return HttpResponse('Same')
            if payee_customer.exists():
                return HttpResponse('Exists') """
        customer_id = request.user.pk

        card = get_object_or_404(Card, Customer_id=request.user.pk)

        transaction_time = timezone.now()

        comment = json_details['comment']  ##get from json

        amount = Decimal(json_details['amount'])  ##get from json

        termini = json_details['termini']  ##get from json

        category = 'Dining Out'  ##get from json

        new_balance = get_new_balances(customer_id, -1, amount)

        method = 'Card Transaction'

        print(comment, amount, termini)

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



def StuShopRender(request):
    return render(request,'FakeTransactions/transactionPage.html')



    ##Create a form for the CardTransactions. look at dashboard forms.py for help
