import datetime
import random
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.generic import DetailView, ListView, CreateView, DeleteView, UpdateView, FormView
from .forms import *
from dashboard.models import *
from django_otp.decorators import otp_required
from dashboard.card_gen import credit_card_number
from django.http.response import JsonResponse
from django.db.models import Q
import json

"""
request is not a visible parameter with Class-based views because as_view() on the .urls file makes the view callable
meaning it takes a request and returns a response
"""


class UserDashboardView(LoginRequiredMixin, DetailView):
    """Redirects the user to dashboard_home if authenticated or the login page otherwise
    Inherits:
        DetailView: inherited class to override the get_object(), get_queryset() and set the Model/template
        LoginRequiredMixin: inherited class used to redirect if not authenticated
    Attributes:
        model = model used with this view
        queryset: queryset which will be returned to the URL that called this view
        template_name: html file to be sent with the response
        context_object_name: variable used on the template to access the context sent with the response
    """
    model = Transaction

    def get_queryset(self):
        """gets all the transactions as we set the view 'model = Transaction'
        :return: all transactions
        """
        return super(UserDashboardView, self).get_queryset()

    def get_object(self, queryset=None):
        """ checks if the current user is a helper or customer and sets the template_name accordingly
        :param request: HttpRequest object containing metadata and current user attributes
        """
        if (self.request.user.is_customer):
            UserDashboardView.template_name = 'dashboard/customer/customer_dashboard.html'
        else:
            UserDashboardView.template_name = 'dashboard/helper/helper_dashboard.html'

    def get_context_data(self, **kwargs):
        """gets the transactions in and out of an account adds them to the context

        :param kwargs: used to obtain the queryset
        :return context: dictionary containing the transactions in an out of the account
        """
        context = super(UserDashboardView, self).get_context_data(**kwargs)
        # get the customer's transactions which are ordered by most recent transaction first
        context['customer_transactions'] = Transaction.objects.filter(Customer_id=self.request.user.pk).order_by(
            '-TransactionTime')
        context['card'] = Card.objects.filter(Customer_id=self.request.user.pk)
        return context


def get_expiry_date():
    """gets the date in 5 years time

    :return datetime of the date now + 5 years:
    """
    now = timezone.now().date()
    return now + datetime.timedelta(days=1825)


def get_CVC():
    """randomises 3 digits to generate a CVC

    :return string array CVC:
    """
    generator = random.Random()
    generator.seed()
    digit_str = []
    for i in range(3):
        digit = str(generator.choice(range(0, 10)))
        digit_str.append(digit)

    return digit_str


def get_card(request):
    """creates a card object for the user that called this method on their dashboard

    :param request: HttpRequest object containing metadata and current user attributes
    :return HttpResponseRedirect: redirects user to the dashboard
    """
    generator = random.Random()
    generator.seed()
    card_num = int(credit_card_number(generator, 16, 1)[0])

    # validation to ensure unique card numbers
    while (Card.objects.filter(CardNum=card_num).exists()):
        card_num = int(credit_card_number(generator, 16, 1)[0])

    mask = "xxxxxxxxxxxx"
    digits = str(card_num)[11:]
    masked_card_num = mask + digits
    card = Card.objects.create(Customer_id=request.user.id, CardNum=card_num, MaskCardNum=masked_card_num,
                               CVC=''.join(get_CVC()),
                               ExpiryDate=get_expiry_date())
    card.save()
    return HttpResponseRedirect(reverse('dashboard_home'))


class PayeeDetailView(LoginRequiredMixin, DetailView):
    """Displays all payees related to the current customer's pk

    Inherits:
        DetailView: inherited class to override the get_object(), get_queryset() and set the Model/template

    Attributes:
        model = model used with this view
        queryset: queryset which will be returned to the URL that called this view
        template_name: html file to be sent with the response
        context_object_name: variable used on the template to access the context sent with the response
    """
    model = Payee
    context_object_name = 'payee_list'
    template_name = 'dashboard/customer/payee_dashboard.html'

    def get_queryset(self):
        """gets the queryset of all the payees

        :return:
        """
        return super(PayeeDetailView, self).get_queryset()

    def get_object(self, queryset=None):
        """refines to queryset to only show the payees related to the current user's pk
        :param request: HttpRequest object containing metadata and current user attributes
        :return: queryset of customer's payees
        """
        return self.get_queryset().filter(User_id=self.request.user.pk)


@login_required
def delete_payee(request, pk):
    """deletes a payee

    :param request: HttpRequest object containing metadata and current user attributes
    :param pk: primary key in the payee table used to identify a specific row
    :return response: HttpResponse object which redirects to new url path
    """
    Payee.objects.filter(pk=pk).delete()
    response = redirect(reverse('viewpayee'))
    return response


@csrf_exempt
def check_payee(request):
    if request.method == "POST":
        str_details = request.body.decode('UTF-8')
        json_details = json.loads(str_details)
        try:
            payee_customer = Customer.objects.filter(sort_code=json_details['sort_code'],
                                                     account_num=json_details['account_num'],
                                                     user__first_name=json_details['firstname'],
                                                     user__last_name=json_details['lastname'])

            if payee_customer[0] == request.user.customer:
                return HttpResponse('Same')
            if payee_customer.exists():
                return HttpResponse('Exists')
        except:
            return HttpResponse('None')


@login_required
def add_payee(request):
    """adds a payee using the POSTed inputs from the PayeeDetailsForm

    :param request: HttpRequest object containing metadata and current user attributes
    :return response: render HttpResponse object which takes request, template name and a dictionary as parameters
    """
    # if this is a POST request and valid then process the form data
    form = PayeeDetailsForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        # getting the cleaned data from the form
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        sort_code = form.cleaned_data['sort_code']
        account_num = form.cleaned_data['account_num']

        try:
            # this attempts to find ane existing customer with details matching the form inputs
            payee_customer_object = Customer.objects.filter(sort_code=sort_code, account_num=account_num,
                                                            user__first_name=first_name, user__last_name=last_name)

            # getting the payee's pk from the queryset of customer objects
            payee_customer_pk = payee_customer_object[0].pk

            # getting the user's pk from the request's user attribute
            user_pk = request.user.pk

            # creating the payee object
            p = Payee(PayeeID_id=payee_customer_pk, User_id=user_pk)

            # persisting the payee object
            p.save()

            # redirecting the user to view the payee they just added
            return HttpResponseRedirect(reverse('viewpayee'))
        except:
            # if an error occurred during addition of the payee then error details are set to aid the user
            error_title = 'Could not add payee!'
            resolution = 'Did you enter the correct details? Sort code should be in the form DD-DD-DD with hyphens included.'

            # a rendered response is returned as a error.html page with accompanying dictionary containing details about the error
            return render(request, 'dashboard/customer/error.html',
                          {'error_title': error_title, 'resolution': resolution})

    # if the request is not POST then render a response with the form on the add_payee.html page
    return render(request, 'dashboard/customer/add_payee.html', {'form': form})


def get_new_balances(customers_customer_id, payees_customer_id, amount):
    # get the customer's customer object using their primary key
    customer = Customer.objects.filter(pk=customers_customer_id)

    # cust_balance is the current balance of the customer
    cust_balance = customer[0].balance

    # cust_new_balance is the balance of the customer after removing the amount they are transferring
    cust_new_balance = cust_balance - amount

    if payees_customer_id != -1:
        # get the payees's customer object using their primary key
        payee = Customer.objects.filter(pk=payees_customer_id)

        # payee_balance is the current balance of the payee
        payee_balance = payee[0].balance

        # payee_new_balance is the balance of the customer after adding the amount they are receiving
        payee_new_balance = payee_balance + amount
    else:
        # if performing a card transaction the payee balance will not need to change as no payee is involved
        payee_new_balance = 0

    new_balances = [cust_new_balance, payee_new_balance]

    return new_balances


def alter_balance(customers_customer_id, new_balance):
    """ changes the balance of the sender/customer and the receiver/payee

    :param customers_customer_id: primary key of the user
    :param new_balance: updated balance
    :return:
    """
    # reduce customer's balance
    # persisting the changed balance in the database
    user = Customer.objects.get(pk=customers_customer_id)
    user.balance = new_balance
    user.save()

    update_available_balance(user)


@login_required
def payee_transfer(request):
    """transfers a sum of money between a customer and one of their payee's using the POSTed inputs from the TransferForm

    :param request: HttpRequest object containing metadata and current user attributes
    :return:
    """
    # if this is a POST request then process the Form data
    if request.method == 'POST':

        # create a form instance and populate it with data from the request
        form = TransferForm(request.user, data=request.POST)
        # check if the form is valid before accessing the data
        if form.is_valid:
            # getting the Payee primary key field
            payee_id = form.data['Payee']

            # using the payee_id to access the payee's user attribute
            payee_object = Payee.objects.filter(id=payee_id)

            # getting the payee's first and last name from the
            payee_fname = payee_object[0].PayeeID.user.first_name
            payee_lname = payee_object[0].PayeeID.user.last_name

            # getting the payee's customer id from the payee_object
            payees_customer_id = payee_object[0].PayeeID_id

            # getting the customer's customer from the request's user attributes
            customers_customer_id = request.user.pk

            # parsing the Amount data to a Decimal as this is required to alter the balance
            amount = Decimal(form.data['Amount'])

            # setting the transaction_time to the current time
            transaction_time = timezone.now()

            # getting the comment data from the form
            comment = form.data['Comment']

            new_balances = get_new_balances(customers_customer_id, payees_customer_id, amount)

            # Termini is the main attribute to view in a transaction e.g. who you transferred the
            # money to/received the money from
            payee_termini = payee_fname + " " + payee_lname

            customer_termini = request.user.first_name + " " + request.user.last_name

            # getting the category data from the form
            category = form.data['Category']

            # default method is Bank Transfer
            method = 'Bank Transfer'

            # creating the transaction object for customer and payee with all the above variables
            # inserted into their matching fields
            customer_transaction = Transaction(Payee_id=payees_customer_id, Customer_id=customers_customer_id,
                                               Amount=amount,
                                               Direction='Out', TransactionTime=transaction_time, Comment=comment,
                                               NewBalance=new_balances[0], Termini=payee_termini, Category=category,
                                               Method=method)

            payee_transaction = Transaction(Payee_id=customers_customer_id, Customer_id=payees_customer_id,
                                            Amount=amount,
                                            Direction='In', TransactionTime=transaction_time, Comment=comment,
                                            NewBalance=new_balances[1], Termini=customer_termini, Category=category,
                                            Method=method)
            print(amount)
            print(new_balances[0])
            try:
                if (amount < 1.00 or request.user.customer.balance-amount < 0):
                    raise
                else:
                    # persisting the transaction object
                    customer_transaction.save()
                    payee_transaction.save()

                    # changing the balance for both the customer and payee
                    alter_balance(customers_customer_id, new_balances[0])
                    alter_balance(payees_customer_id, new_balances[1])

                    # redirecting the user to the dashboard to view the transaction
                    return HttpResponseRedirect(reverse('dashboard_home'))

            except:
                # If an error occurred during persistence of the transaction or altering of the balance
                error_title = 'Could not complete transaction!'
                resolution = 'Is your balance correct? Is the amount equal to or above £1.00?'

                # a rendered response is returned as a error.html page with accompanying dictionary containing details about the error
                return render(request, 'dashboard/customer/error.html',
                              {'error_title': error_title, 'resolution': resolution})

    # if the request is a GET then create the default form, request.user must be sent so that __init_ has
    # access to the user's pk to get all the payee's
    else:
        form = TransferForm(request.user)

    # setting the context to the form
    context = {
        'form': form,
    }

    # returning the rendered transfer.html with the form inside the context
    return render(request, 'dashboard/customer/transfer.html', context)


@login_required
def card_transaction(request):
    """transfers a sum of money between a customer and one of their payee's using the POSTed inputs from the TransferForm

        :param request: HttpRequest object containing metadata and current user attributes
        :return:
        """
    # if this is a POST request then process the Form data
    if request.method == 'POST':

        # create a form instance and populate it with data from the request
        form = CardTransaction(request.user, data=request.POST)
        # check if the form is valid before accessing the data
        if form.is_valid:
            # getting the Card id
            card_id = form.data['Card']

            # getting the Customer id from the request attributes
            customer_id = request.user.pk

            # parsing the Amount data to a Decimal as this is required to alter the balance
            amount = Decimal(form.data['Amount'])

            # setting the transaction_time to the current time
            transaction_time = timezone.now()

            # getting the comment data from the form
            comment = form.data['Comment']

            termini = form.data['Termini']

            category = form.data['Category']

            new_balance = get_new_balances(customer_id, -1, amount)

            method = 'Card Transaction'

            card_transaction_object = Transaction(Card_id=card_id, Customer_id=customer_id,
                                                  Amount=amount,
                                                  Direction='Out', TransactionTime=transaction_time, Comment=comment,
                                                  NewBalance=new_balance[0], Termini=termini, Category=category,
                                                  Method=method)
            try:
                if (amount < 1.00):
                    raise
                else:
                    # persisting the transaction object
                    card_transaction_object.save()

                    # changing the balance for both the customer and payee
                    alter_balance(customer_id, new_balance[0])

                    # redirecting the user to the dashboard to view the transaction
                    return HttpResponseRedirect(reverse('dashboard_home'))

            except:
                # If an error occurred during persistence of the transaction or altering of the balance
                error_title = 'Could not complete transaction!'
                resolution = 'Is your balance correct? Is the amount equal to or above £1.00?'

                # a rendered response is returned as a error.html page with accompanying dictionary containing details about the error
                return render(request, 'dashboard/customer/error.html',
                              {'error_title': error_title, 'resolution': resolution})

    # if the request is a GET then create the default form, request.user must be sent so that __init_ has
    # access to the user's pk to get all the payee's
    else:
        form = CardTransaction(request.user)

    # setting the context to the form
    context = {
        'form': form,
    }

    # returning the rendered transfer.html with the form inside the context
    return render(request, 'dashboard/customer/spoof_transaction.html', context)


def livechat(request, pk):
    """this method returns all the message objects between two users and renders them on livechat.html with the relevant
    context

    :param request: HttpRequest object containing metadata and current user attributes
    :param pk: the primary key of the other user in the livechat
    :return render: rendered livechat.html template with messages and other_user as context
    """
    other_user = get_object_or_404(User, pk=pk)
    messages = Message.objects.filter(
        Q(receiver=other_user, sender=request.user) | Q(receiver=request.user, sender=other_user)
    ).order_by("created_at")
    return render(request, 'dashboard/customer/livechat.html', {"other_user": other_user, "messages": messages})


@csrf_exempt
# TODO: csrf_exempt must be temporary to prevent cross site scripting attacks
def message(request, pk):
    """This method creates method objects if the have been POSTed from one of the users in the livechat.
    If the method is GET then the unseen messages are returned.

    :param request: HttpRequest object containing metadata and current user attributes
    :param pk: Primary key of the other user in the livechat
    :return HttpResponse/JsonResponse:
    'Added' is returned once the message is persisted into the database if the request method is POST.
    JSON objects of the new unseen messages are returned if the request method is GET.
    """
    other_user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        message = json.loads(request.body)
        m = Message(receiver=other_user, sender=request.user, message=message, created_at=timezone.now())
        m.save()
        result = {
            "message": m.message,
            "sender": m.sender.username,
            "time": naturaltime(m.created_at),
            "sent": True
        }
        return JsonResponse(result, safe=False)
    elif request.method == "GET":
        messages = Message.objects.filter(seen=False, receiver=request.user)
        results = []
        for message in messages:
            result = {
                "message": message.message,
                "sender": message.sender.username,
                "time": naturaltime(message.created_at),
                "sent": False
            }
            results.append(result)
        messages.update(seen=True)
        return JsonResponse(results, safe=False)


'''
MONEY POT STUFF ( ͡° ͜ʖ ͡°)
- Money pot displays notice when target has been met
- Display percentage complete of each pot
'''


class MoneyPotListView(LoginRequiredMixin, ListView):
    model = MoneyPot
    template_name = 'dashboard/customer/money_pots.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        customer = Customer.objects.get(user=self.request.user)
        context = super().get_context_data(**kwargs)
        context['money_pots'] = MoneyPot.objects.filter(customer=customer)
        return context


class MoneyPotCreateView(LoginRequiredMixin, CreateView):
    template_name = 'dashboard/customer/money_pots_add.html'
    model = MoneyPot
    fields = ['name', 'target_balance']
    success_url = '/dashboard/moneypots/'

    def form_valid(self, form):
        customer = Customer.objects.get(user=self.request.user)
        form.instance.customer = customer
        return super(MoneyPotCreateView, self).form_valid(form)


class MoneyPotDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'dashboard/customer/money_pots_confirm_delete.html'
    model = MoneyPot
    success_url = '/dashboard/moneypots/'

    # If money pot is deleted, update the available balance
    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        customer = Customer.objects.get(user=self.request.user)
        update_available_balance(customer)
        return redirect('money_pots')


class MoneyPotUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'dashboard/customer/money_pots_update.html'
    model = MoneyPot
    fields = ['name', 'target_balance']
    success_url = '/dashboard/moneypots/'


class MoneyPotDepositView(LoginRequiredMixin, FormView):
    template_name = 'dashboard/customer/money_pots_deposit.html'
    form_class = DepositForm
    success_url = '/dashboard/moneypots/'

    def form_valid(self, form):
        customer = Customer.objects.get(user=self.request.user)
        amount = form.cleaned_data.get('amount')

        if (customer.available_balance - amount) < 0:
            # Customer doesn't have enough funds to deposit
            print('Not enough money')
        else:
            # Customer has enough funds to deposit
            pk = self.kwargs['pk']
            money_pot = MoneyPot.objects.get(pk=pk)

            # Add deposited amount to money pot
            money_pot.pot_balance += amount
            money_pot.save()

            # Update customers available balance
            update_available_balance(customer)

        return super(MoneyPotDepositView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        money_pot = MoneyPot.objects.get(pk=pk)

        context = super().get_context_data(**kwargs)

        context['pot'] = money_pot
        return context


# Update the available balance of the customer. Any money not in a money pot is available to spend
def update_available_balance(customer):
    money_pots_total = 0
    money_pots = MoneyPot.objects.filter(customer=customer)

    # Add up the current balances of all the customers pots
    for pot in money_pots:
        money_pots_total += pot.pot_balance

    # Find the balance the customer can spend by subtracting all money pot balances from main balance
    available_balance = customer.balance - money_pots_total
    customer.available_balance = available_balance
    customer.save()

# class TransactionListView(ListView):
#     model = Transaction
#     context_object_name = 'transaction_list'
#     template_name = 'dashboard/customer/transactions.html'
#
#
# class TransactionDetailView(DetailView):
#     model = Transaction
#     context_object_name = 'transaction_list'
#     template_name = 'dashboard/customer/transactions.html'
#
#
#     def get_queryset(self):
#         return super(TransactionDetailView, self).get_queryset()
#
#     def get_object(self):
#         return self.get_queryset().filter(Customer_id=self.request.user.pk)
