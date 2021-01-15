from django.http import *
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import View
from FakeTransactions.forms import *
from FakeTransactions.models import Category, Product
from dashboard.models import *
from decimal import Decimal


# Create your views here.
def AddNewTransaction(request):
    t = Transaction
    food_context = {'form': TransactionForm()}
    products = Product.objects.all()
    categories = Category.objects.all()
    context = {'products': products, 'categories': categories}

   #if request.method=="POST":
        #if request.Post.get('price'):

    return render(request, 'FakeTransactions/transactionPage.html', context)

    ##Create a form for the CardTransactions. look at dashboard forms.py for help
