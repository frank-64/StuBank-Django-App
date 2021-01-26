import datetime
import io
import random
import csv
import collections
import matplotlib.pyplot as plotter

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, DeleteView, UpdateView, FormView
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from .decorators import valid_helper
from .forms import *
from dashboard.models import *
from dashboard.card_gen import credit_card_number
from django.http.response import JsonResponse
from django.db.models import Q
import json
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Frame, PageTemplate, FrameBreak, \
    Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

"""
Request is not a visible parameter with Class-based views because as_view() on the .urls file makes the view callable
meaning it takes a request and returns a response
"""


@method_decorator(login_required, name='dispatch')
class UserDashboardView(LoginRequiredMixin, DetailView):
    """
        Written by: Frankie
        Redirects the user to dashboard_home if authenticated or the login page otherwise
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
        """
            Written by: Frankie
            Gets all the transactions as we set the view 'model = Transaction'
            :return: all transactions
        """
        return super(UserDashboardView, self).get_queryset()

    def get_object(self, queryset=None):
        """
            Written by: Frankie
            Checks if the current user is a helper or customer and sets the template_name accordingly
            :param request: HttpRequest object containing metadata and current user attributes
        """
        if (self.request.user.is_customer):
            UserDashboardView.template_name = 'dashboard/customer/customer_dashboard.html'
        else:
            UserDashboardView.template_name = 'dashboard/helper/helper_chats.html'

    def get_context_data(self, **kwargs):
        """
            Written by: Frankie
            gets the transactions in and out of an account adds them to the context

            :param kwargs: used to obtain the queryset
            :return context: dictionary containing the transactions in an out of the account
        """
        context = super(UserDashboardView, self).get_context_data(**kwargs)
        if (self.request.user.is_customer):
            # get the customer's transactions which are ordered by most recent transaction first
            context['customer_transactions'] = Transaction.objects.filter(Customer_id=self.request.user.pk).order_by(
                '-TransactionTime')
            context['card'] = Card.objects.filter(Customer_id=self.request.user.pk)
        else:
            context['livechats'] = LiveChat.objects.filter(helper_id=self.request.user.id)
        return context


def get_expiry_date():
    """
        Written by: Frankie
        Gets the date in 5 years time

        :return datetime of the date now + 5 years:
    """
    now = timezone.now().date()
    return now + datetime.timedelta(days=1825)


def get_CVC():
    """
        Written by: Frankie
        Randomises 3 digits to generate a CVC

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
    """
        Written by: Frankie
        Creates a card object for the user that called this method on their dashboard

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
    """
        Written by: Frankie
        Displays all payees related to the current customer's pk

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
        """ Gets the queryset of all the payees

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
    """
        Written by: Frankie
        Deletes a payee

        :param request: HttpRequest object containing metadata and current user attributes
        :param pk: primary key in the payee table used to identify a specific row
        :return response: HttpResponse object which redirects to new url path
    """
    Payee.objects.filter(pk=pk).delete()
    response = redirect(reverse('viewpayee'))
    return response


# TODO: Remove csrf_exempt
@csrf_exempt
def check_payee(request):
    """
        Written by: Frankie
        Checks the details POSTed through the request.body and parses it to a JSON object which can be checked to see
        if the payee exists

        :param request: HttpRequest object containing metadata and current user attributes
        :return: 'Same' if the user attempts to add themselves, 'Exists' if the user has already added this payee or
                 'Valid' if the payee is valid.
    """
    if request.method == "POST":
        # Decode the request body into a string
        str_details = request.body.decode('UTF-8')

        # Convert the string to a JSON object
        json_details = json.loads(str_details)
        try:
            # Get the customer with matching details from the JSON
            payee_customer = Customer.objects.filter(sort_code=json_details['sort_code'],
                                                     account_num=json_details['account_num'],
                                                     user__first_name=json_details['firstname'],
                                                     user__last_name=json_details['lastname'])

            # Getting the customer object from the filtered customer objects
            customer_object = payee_customer[0]

            # Getting the payee object of the current user and the user they're attempting to add to see if there is a
            # duplicate
            existing_payee_list = Payee.objects.filter(User_id=request.user.pk, PayeeID_id=customer_object)

            # If the customer attempts to add themselves as a payee return 'Same'
            if customer_object == request.user.customer:
                return HttpResponse('Same')
            # If the payee has already been added return 'Exists'
            elif payee_customer.exists() and len(existing_payee_list) > 0:
                return HttpResponse('Exists')

            # If the payee exists and is not already a current payee
            elif payee_customer.exists():
                return HttpResponse('Valid')
        except:
            print("Error")
            return HttpResponse('None')


@login_required
def add_payee(request):
    """
        Written by: Frankie
        Adds a payee using the POSTed inputs from the PayeeDetailsForm

        :param request: HttpRequest object containing metadata and current user attributes
        :return response: render HttpResponse object which takes request, template name and a dictionary as parameters
    """
    # if this is a POST request and valid then process the form data
    form = PayeeDetailsForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        # getting the cleaned data from the form
        first_name = form.data['first_name']
        last_name = form.data['last_name']
        sort_code = form.data['sort_code']
        account_num = form.data['account_num']

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


# TODO: Remove csrf_exempt
@csrf_exempt
def card_verification(request):
    """
        Written by: Frankie
        This function verifies the current user know their card details and returns valid if the details they entered
        matches their current card.

        :param request:
        :return:
    """

    if request.method == "POST":
        # Decode the request body into a string
        str_details = request.body.decode('UTF-8')

        # Convert the string into a json object
        json_details = json.loads(str_details)
        try:
            # Get the card of the current user
            customer_card = get_object_or_404(Card, Customer_id=request.user.pk)

            # Get the card from the details the user entered
            verify_card = Card.objects.filter(CVC=json_details['CVC'], ExpiryDate=json_details['expiry_date'])

            # Verify the two cards match and return valid
            if (verify_card[0] == customer_card) and (not customer_card.CardFrozen):
                return HttpResponse('Valid')
            elif (customer_card.CardFrozen):
                return HttpResponse('Frozen')
            else:
                return HttpResponse('Invalid')
        except:
            return HttpResponse('None')


def get_new_balances(customers_customer_id, payees_customer_id, amount):
    """
        Written by: Frankie
        This method gets the new balances of the customer and payee once the amount has been removed from the customer's
        balance and added to the payee's balance.
        If payee_customer_id = -1 then only remove the balance from the customer as a card transaction is being used,
        which, in our scenario, does not have anyone to receive the money.

        :param customers_customer_id: The primary key of the customer
        :param payees_customer_id: The primary key of the payee
        :param amount: The amount to increase or decrease the balances by
        :return: A list of the new balances
    """
    # get the customer's customer object using their primary key
    customer = Customer.objects.filter(pk=customers_customer_id)

    # cust_balance is the current balance of the customer
    cust_balance = customer[0].balance

    # cust_new_balance is the balance of the customer after removing the amount they are transferring
    cust_new_balance = cust_balance - amount

    if payees_customer_id != -1:
        # get the payee's customer object using their primary key
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
    """
        Written by: Frankie
        Changes the balance of the sender/customer and the receiver/payee

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
    """
        Written by: Frankie with additions from Ed
        Transfers a sum of money between a customer and one of their payee's using the POSTed inputs from the TransferForm

        :param request: HttpRequest object containing metadata and current user attributes
        :return:
    """

    customer = Customer.objects.get(user=request.user)
    num_pots = MoneyPot.objects.filter(customer=customer).count()

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
            try:
                if (amount < 1.00 or request.user.customer.balance - amount < 0):
                    raise
                else:

                    # persisting the transaction object
                    customer_transaction.save()
                    payee_transaction.save()

                    # changing the balance for both the customer and payee
                    alter_balance(customers_customer_id, new_balances[0])
                    alter_balance(payees_customer_id, new_balances[1])

                    # Add the rounded up amount to the money pot
                    round_up_amount = request.POST.get('amount')
                    if round_up_amount != "0":
                        pot_id = form.data['pot']

                        pot = MoneyPot.objects.get(pk=pot_id)
                        pot.pot_balance += Decimal(round_up_amount)
                        pot.save()

                        customer = Customer.objects.get(pk=customers_customer_id)
                        payee = Customer.objects.get(pk=payees_customer_id)
                        update_available_balance(customer)
                        update_available_balance(payee)

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
        'num_pots': num_pots
    }

    # returning the rendered transfer.html with the form inside the context
    return render(request, 'dashboard/customer/transfer.html', context)


@login_required
def card_transaction(request):
    """
        Written by: Frankie
        Transfers a sum of money between a customer and one of their payee's using the POSTed inputs from the TransferForm

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
                if amount < 1.00:
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

                # a rendered response is returned as a error.html page with accompanying dictionary containing
                # details about the error
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


@login_required
def livechat(request, pk):
    """
    Written by: Frankie This method returns all the message objects between two users and renders them on
    customer_livechat.html with the relevant context

        :param request: HttpRequest object containing metadata and current user attributes
        :param pk: the primary key of the other user in the livechat
        :return render: rendered customer_livechat.html template with messages and other_user as context
    """

    # this checks if a livechat already exists between the current user (request.user.id) and the user with
    # primary key = pk
    livechat = None

    # other_user is the other user relative to the current user in the livechat which the current user intends to
    # communicate with
    helper = False
    other_user = get_object_or_404(User, pk=pk)
    if (not other_user.is_helper):
        livechat = LiveChat.objects.filter(customer_id=other_user.pk, helper_id=request.user.pk, is_active=True)
        helper = True
    else:
        livechat = LiveChat.objects.filter(customer_id=request.user.pk, helper_id=other_user.pk, is_active=True)

    # this obtains all the messages sent and received between the current user and the other user
    messages = Message.objects.filter(
        Q(receiver=other_user, sender=request.user) | Q(receiver=request.user, sender=other_user)
    ).order_by("created_at")

    # this condition redirects the user to the customer_livechat template if they are a customer and have a
    # LiveChat object with a helper. If the user is a helper they are redirected to the helper template. Otherwise an
    # error is displayed.
    if helper == False and livechat.exists():
        return render(request, 'dashboard/customer/customer_livechat.html',
                      {"other_user": other_user, "messages": messages, "livechat": livechat})
    elif not other_user.is_helper and livechat.exists():
        card = get_object_or_404(Card, Customer_id=other_user.pk)
        return render(request, 'dashboard/helper/helper_livechat.html',
                      {"card": card, "other_user": other_user, "messages": messages, "livechat": livechat})
    else:
        error = "The Livechat could not be accessed."
        resolution = "Have you requested assistance and clicked the link on the Help page?"
        return render(request, 'dashboard/customer/error.html',
                      {"error": error, "resolution": resolution})


@login_required
@csrf_exempt
# TODO: csrf_exempt must be temporary to prevent cross site scripting attacks
def message(request, pk):
    """
        Written by: Frankie
        This method creates method objects if the have been POSTed from one of the users in the livechat.
        If the method is GET then the unseen messages are returned.

        :param request: HttpRequest object containing metadata and current user attributes
        :param pk: Primary key of the other user in the livechat
        :return HttpResponse/JsonResponse:
        'Added' is returned once the message is persisted into the database if the request method is POST.
        JSON objects of the new unseen messages are returned if the request method is GET.
    """

    # This checks if a livechat already exists between the current user (request.user.id) and the user with
    # primary key = pk
    other_user = get_object_or_404(User, pk=pk)

    # If the request is POST add the message to the database and return the message the sender needs to see on their
    # client. If the request is GET then return all the unseen messages where the current user is the receiver.

    if request.method == "POST":
        message = json.loads(request.body)

        # Creating the message objects and persisting it to the database
        m = Message(receiver=other_user, sender=request.user, message=message, created_at=timezone.now())
        m.save()
        result = {
            "message": m.message,
            "sender": m.sender.first_name,
            "time": naturaltime(m.created_at),
            "sent": True
        }

        # Returning the JSON object to be displayed on the livechat of the sender
        return JsonResponse(result, safe=False)
    elif request.method == "GET":
        messages = Message.objects.filter(seen=False, receiver=request.user)
        results = []
        for message in messages:
            result = {
                "message": message.message,
                "sender": message.sender.first_name,
                "time": naturaltime(message.created_at),
                "sent": False
            }
            results.append(result)

        # As all new messages have been added to the results seen must be made True so the same messages are not
        # retrieved again next time
        messages.update(seen=True)

        # Returnin the JSON object of all the unseen messages
        return JsonResponse(results, safe=False)


@login_required
def help_page(request):
    """
    Written by: Frankie
    This method renders the help.html page on the dashboard

    :param request: HttpRequest object containing metadata and current user attributes
    :return:
    """
    return render(request, 'dashboard/customer/help.html')


@login_required
def get_helper(request):
    """
        Written by: Frankie
        This function gets the primary key of a helper for the customer to use to join the live chat with the helper

        :param request: HttpRequest object containing metadata and current user attributes
        :return: The primary key of the helper the user has an active livechat with
    """

    # If there is an existing and active livechat object with the customer_id as the current user's pk then return
    # the pk of the existing helper in that livechat
    if LiveChat.objects.filter(customer_id=request.user.id, is_active=True).exists():
        existing_chat = LiveChat.objects.filter(customer_id=request.user.id, is_active=True)
        return HttpResponse(existing_chat.first().helper.pk)

    # If the customer does not have an existing livechat then create a LiveChat object and return the helper's pk
    else:
        helpers = Helper.objects.all()
        random_helper = random.choice(helpers)
        lc = LiveChat(customer_id=request.user.id, helper_id=random_helper.pk)
        lc.save()
        return HttpResponse(random_helper.pk)


@login_required
def grant_permission(request, pk):
    """
        Written by: Frankie
        This function is used by customers to grant permission to a helper in a livechat

        :param request: HttpRequest object containing metadata and current user attributes
        :return: HttpResponse 'Done' if successful or redirected to the dashboard if the livechat doesn't exist
    """
    # Checking if a livechat exists between the current customer from request and the helper with primary key = pk
    lc = LiveChat.objects.filter(customer_id=request.user.pk, helper_id=pk, is_active=True)
    if lc.exists():
        # Updating the permissions
        lc.update(perm_granted=True)
        return HttpResponse('Done')
    else:
        return HttpResponseRedirect(reverse('dashboard_home'))


@valid_helper
def deactivate_livechat(request, pk):
    """
        Written by: Frankie
        This function is used by the helper to deactivate a livechat

        :param request: HttpRequest object containing metadata and current user attributes
        :return: HttpResponseRedirect to the dashboard
    """
    # Checking if a livechat exists between the current helper from request and the customer with primary key = pk
    livechat = LiveChat.objects.filter(helper_id=request.user.pk, customer=pk, is_active=True, perm_granted=True)
    if livechat.exists():
        livechat.update(is_active=False)
    return HttpResponseRedirect(reverse('dashboard_home'))


@valid_helper
def toggle_account_frozen(request, pk):
    """
        Written by: Frankie
        This function is used by the helper to freeze and unfreeze a customer's account.

        :param request: HttpRequest object containing metadata and current user attributes
        :return: HttpResponseRedirect to the livechat once successful
    """
    # Checking if a livechat exists between the current helper from request and the customer with primary key = pk
    livechat_exists = LiveChat.objects.filter(helper_id=request.user.pk, customer_id=pk, is_active=True,
                                              perm_granted=True).exists()
    if livechat_exists:
        user = get_object_or_404(User, pk=pk)
        if user.is_active:
            User.objects.filter(pk=pk).update(is_active=False)
            return HttpResponseRedirect(reverse('livechat', args=(pk,)))
        else:
            User.objects.filter(pk=pk).update(is_active=True)
            return HttpResponseRedirect(reverse('livechat', args=(pk,)))
    else:
        return HttpResponseRedirect(reverse('dashboard_home'))


@valid_helper
def toggle_card_frozen(request, pk):
    """
        Written by: Frankie
        This function is used by the helper to freeze and unfreeze a customer's card.

        :param request: HttpRequest object containing metadata and current user attributes
        :return: HttpResponseRedirect to the livechat once successful
    """
    # Checking if a livechat exists between the current helper from request and the customer with primary key = pk
    livechat_exists = LiveChat.objects.filter(helper_id=request.user.pk, customer_id=pk, is_active=True,
                                              perm_granted=True).exists()
    if livechat_exists:

        # Gets the Card object related to that user
        card = get_object_or_404(Card, Customer_id=pk)

        # If the card is frozen then unfreeze it and redirect to the dashboard and vice versa
        if card.CardFrozen:
            Card.objects.filter(Customer_id=pk).update(CardFrozen=False)
            return HttpResponseRedirect(reverse('livechat', args=(pk,)))
        else:
            Card.objects.filter(Customer_id=pk).update(CardFrozen=True)
            return HttpResponseRedirect(reverse('livechat', args=(pk,)))
    else:
        return HttpResponseRedirect(reverse('dashboard_home'))


@login_required
def customer_card_frozen(request):
    """
        Written by: Frankie
        This is a toggleable function which the customer uses to freeze and unfreeze their card

        :param request: HttpRequest object containing metadata and current user attributes
        :return: HttpResponseRedirect to the dashboard
    """
    # Get the primary get of the current user from request
    pk = request.user.pk

    # Gets the Card object related to user with primary key = pk
    card = get_object_or_404(Card, Customer_id=pk)

    # If the card is frozen then unfreeze it and redirect to the dashboard and vice versa
    if card.CardFrozen:
        Card.objects.filter(Customer_id=pk).update(CardFrozen=False)
        return HttpResponseRedirect(reverse('dashboard_home'))
    else:
        Card.objects.filter(Customer_id=pk).update(CardFrozen=True)
        return HttpResponseRedirect(reverse('dashboard_home'))


@method_decorator(valid_helper, name='dispatch')
class LiveChatTransactions(DetailView):
    """
        Written by: Frankie
        This class displays transactions to the helper for a given customer in the live chat

        :param request: HttpRequest object containing metadata and current user attributes
        :return: a queryset of all the customer's transactions and renders them on transactions.html
    """
    model = Transaction
    context_object_name = 'transaction_list'
    template_name = 'dashboard/customer/transactions.html'

    def get_queryset(self):
        return super(LiveChatTransactions, self).get_queryset()

    def get_object(self):
        # Getting the primary key from the url
        pk = self.kwargs['pk']

        # Checking the livechat exists
        livechat_exists = LiveChat.objects.filter(helper_id=self.request.user.pk, customer_id=pk, is_active=True,
                                                  perm_granted=True).exists()
        if livechat_exists:
            return self.get_queryset().filter(Customer_id=pk)


'''
MONEY POT STUFF ( ͡° ͜ʖ ͡°)
'''


@method_decorator(login_required, name='dispatch')
class MoneyPotListView(LoginRequiredMixin, ListView):
    """
        Written by: Ed
        Purpose: To display all the customer's currently created money pots as a list
    """

    model = MoneyPot
    template_name = 'dashboard/customer/money_pots.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        customer = Customer.objects.get(user=self.request.user)
        context = super().get_context_data(**kwargs)
        context['money_pots'] = MoneyPot.objects.filter(customer=customer)
        return context


@method_decorator(login_required, name='dispatch')
class MoneyPotCreateView(LoginRequiredMixin, CreateView):
    """
        Written by: Ed
        Purpose: To allow the customer to create a new money pot where they can specify its name and target balance
    """

    template_name = 'dashboard/customer/money_pots_add.html'
    model = MoneyPot
    fields = ['name', 'target_balance']
    success_url = '/dashboard/moneypots/'

    def form_valid(self, form):
        customer = Customer.objects.get(user=self.request.user)
        form.instance.customer = customer
        return super(MoneyPotCreateView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class MoneyPotDeleteView(LoginRequiredMixin, DeleteView):
    """
        Written by: Ed
        Purpose: To allow the customer to delete any previously created money pots, sending any money stored in it back
                into their main account balance
    """

    template_name = 'dashboard/customer/money_pots_confirm_delete.html'
    model = MoneyPot
    success_url = '/dashboard/moneypots/'

    # If money pot is deleted, update the available balance
    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        customer = Customer.objects.get(user=self.request.user)
        update_available_balance(customer)
        return redirect('money_pots')


@method_decorator(login_required, name='dispatch')
class MoneyPotUpdateView(LoginRequiredMixin, UpdateView):
    """
        Written by: Ed
        Purpose: To allow the user to update any of their money pots with a new name or target balance
    """

    template_name = 'dashboard/customer/money_pots_update.html'
    model = MoneyPot
    fields = ['name', 'target_balance']
    success_url = '/dashboard/moneypots/'


@method_decorator(login_required, name='dispatch')
class MoneyPotDepositView(LoginRequiredMixin, FormView):
    """
        Written by: Ed
        Purpose: To allow the user to deposit money into a previously created money pot from their available balance
    """

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
    """
        Written by: Ed
        Purpose: To update the customers available balance to not include any money stored in money pots.
                available_balance = balance - (total $ stored in money pots)
    """

    money_pots_total = 0
    money_pots = MoneyPot.objects.filter(customer=customer)

    # Add up the current balances of all the customers pots
    for pot in money_pots:
        money_pots_total += pot.pot_balance

    # Find the balance the customer can spend by subtracting all money pot balances from main balance
    available_balance = customer.balance - money_pots_total
    customer.available_balance = available_balance
    customer.save()


'''
BANK STATEMENTS STUFF [̲̅$̲̅(̲̅ιοο̲̅)̲̅$̲̅]
'''


@login_required
def pdf_view(request):
    """
        Written by: Ed
        Purpose: To provide a downloadable pdf file displaying all the customers transactions in a neatly formatted
                layout
    """

    user = request.user
    customer = Customer.objects.get(user=user)
    filename = user.username + "_statement.pdf"
    theme_colour = colors.Color(red=(52 / 255), green=(58 / 255), blue=(64 / 255))

    # Initialise HttpResponse which provides user with pdf download when requested
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=' + filename

    # Create initial pdf document
    buffer = io.BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=A4)
    width, height = A4

    # Create frames for use in template
    margin = 50
    active_width = (width - margin * 2)
    frame_padding = 10

    frames = [Frame(margin, height - (margin * 2.5), margin * 2, margin * 1.75, id='logo', showBoundary=0),
              Frame(margin + (margin * 2.5), height - (margin * 2.5), margin * 3, margin * 1.75, id='logo_text',
                    showBoundary=0),
              Frame(width - (margin + margin * 3.5), height - (margin * 2.5), margin * 3.5, margin * 1.75,
                    id='account_details', showBoundary=0),
              Frame(margin, height - (margin * 4), margin * 3, margin * 1.75, id='branch_details', showBoundary=0),
              Frame(margin + (margin * 3 + frame_padding), height - (margin * 4), margin * 3, margin * 1.75,
                    id='personal_details', showBoundary=0),
              Frame(margin + (margin * 6 + 2 * frame_padding), height - (margin * 4), (active_width - (frame_padding *
                                                                                                       2) - (
                                                                                               margin * 6)), margin,
                    id='current_balance', showBoundary=0),
              Frame(margin, margin * 2, active_width, margin * 11, id='statement', showBoundary=0)]

    # Create template and add it to pdf
    template = PageTemplate(id='main', frames=frames)
    pdf.addPageTemplates([template])

    # Elements list which will contain all content to be drawn onto the pdf
    elements = []

    # Create styles that will be assigned to paragraphs for paragraph customisation
    styles = getSampleStyleSheet()
    heading1 = ParagraphStyle('Heading1', fontName='Helvetica-Bold', fontSize=25)
    account_details = ParagraphStyle('details', alignment=2)
    heading2 = ParagraphStyle('Heading2', backColor=theme_colour, alignment=0, textColor=colors.white, fontSize=12,
                              leading=16)
    content1 = ParagraphStyle('content1', alignment=0, fontSize=8)
    balances = ParagraphStyle('balances', alignment=0, fontSize=10)
    small_content = ParagraphStyle('small_print', alignment=0, fontSize=6, leading=8)

    '''
    Add PDF content here ▼
    '''

    # Logo
    logo = Image('static/images/monkey.png')
    logo._restrictSize(margin * 1.75, margin * 1.5)

    # Logo text
    logo_text = Paragraph("Statement", heading1)

    # Account details
    account_details = Paragraph('Account number: <b>' + str(customer.account_num) + '</b><br/>Sort code: <b>' +
                                str(customer.sort_code) + '</b><br/>Username: <b>' + str(user.username) + '</b>',
                                account_details)

    # Branch details
    branch_title = Paragraph('Branch Details', heading2)
    branch_details = Paragraph('StuBank PLC <br/> 21 Canada Crescent <br/> Newcastle upon Tyne <br/> NE2 7BM', content1)

    # Personal Details
    personal_title = Paragraph('Your current details', heading2)
    personal_details = Paragraph(str(user.first_name) + ' ' + str(user.last_name) + '<br/>' + str(user.email), content1)

    # Current balance
    balance = Paragraph('<br/> Current balance: <b>£' + str(customer.balance) + '</b><br/> Available balance: <b>£' +
                        str(customer.available_balance) + '</b>', balances)

    # Retrieve all user's transactions
    transactions = Transaction.objects.filter(Customer_id=user.pk).order_by(
        '-TransactionTime')

    # Build list of lists containing all transaction data to be inserted into statement table
    data = [['Date', 'Method', 'Category', 'Comment', 'Direction', 'Termini', 'Amount', 'New balance']]
    for i in transactions:
        termini = Paragraph(str(i.Termini), styles['Normal'])
        amount = Paragraph(str(i.Amount), styles['Normal'])
        new_balance = Paragraph(str(i.NewBalance), styles['Normal'])
        direction = Paragraph(str(i.Direction), styles['Normal'])
        date = Paragraph(str(i.TransactionTime)[:19], styles['Normal'])
        comment = Paragraph(str(i.Comment), styles['Normal'])
        method = Paragraph(str(i.Method), styles['Normal'])
        category = Paragraph(str(i.Category), styles['Normal'])

        data.append([date, method, category, comment, direction, termini, amount, new_balance])

    # Set table properties and styles
    table = Table(data, repeatRows=1)
    table.setStyle(TableStyle([
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), theme_colour),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ]))

    '''
    End PDF content here ▲
    '''

    # Add the different elements of the PDF to elements list, and use it to build PDF
    elements.extend([logo, FrameBreak()])
    elements.extend([logo_text, FrameBreak()])
    elements.extend([account_details, FrameBreak()])
    elements.extend([branch_title, branch_details, FrameBreak()])
    elements.extend([personal_title, personal_details, FrameBreak()])
    elements.extend([balance, FrameBreak()])
    elements.extend([table, FrameBreak()])
    pdf.build(elements)

    response.write(buffer.getvalue())
    buffer.close()

    return response


'''
EXPENDITURE OVERVIEW STUFF ᶘᵒᴥᵒᶅ
'''


@login_required
def expenditure_overview(request):
    """
        Written by: Ed + Fin
        Purpose: To display a series of charts outlining a customers transaction history, habits and predictions about
        their future spending
    """

    transactions = Transaction.objects.filter(Customer_id=request.user.pk)

    # Categories
    category_name = []
    category_amount = []
    category_dict = dict()

    # Termini's
    termini_name = []
    termini_amount = []
    termini_dict = dict()

    # Outgoings / Income
    out_in_labels = ['Outgoing', 'Income']
    out_in_data = [0, 0]

    # Correctly formatting the transaction data for use in Chart.js
    for transaction in transactions:
        if transaction.Direction == 'Out':
            category_dict[transaction.Category] = category_dict.get(transaction.Category, 0) + float(transaction.Amount)
            termini_dict[transaction.Termini] = termini_dict.get(transaction.Termini, 0) + float(transaction.Amount)
            out_in_data[0] += float(transaction.Amount)
        else:
            out_in_data[1] += float(transaction.Amount)

    for key, value in category_dict.items():
        category_name.append(key)
        category_amount.append(value)

    for key, value in termini_dict.items():
        termini_name.append(key)
        termini_amount.append(value)

        customer_id = "1"
        total = 0
        eveningspend = 0
        afternoonspend = 0
        morningspend = 0
        lastmonth = datetime.datetime.today().replace(day=1) - datetime.timedelta(days=1)
        monthlycategories = collections.Counter()
        categories = collections.Counter()

        with open('data.txt', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for i in csv_reader:
                if i["direction"] == "Out":
                    categories[i["category"]] += 1
                    newtime = i["transactiontime"]
                    newtime = datetime.datetime.strptime(newtime, "%Y-%m-%d %H:%M:%S.%f")
                    if newtime > lastmonth and i["customer_id"] == customer_id:
                        monthlycategories[i["category"]] += 1
                        total += float(i["amount"])
                        if newtime.time() > datetime.datetime.strptime("17:00:00.000000", "%H:%M:%S.%f").time():
                            eveningspend += 1
                        elif datetime.datetime.strptime("12:00:00.000000", "%H:%M:%S.%f").time() < newtime.time() < \
                                datetime.datetime.strptime("17:00:00.000000", "%H:%M:%S.%f").time():
                            afternoonspend += 1
                        else:
                            morningspend += 1

    # Return all correctly formatted data to be transformed into bar charts
    return render(request, 'dashboard/customer/expenditure_overview.html', {
        'category_labels': category_name,
        'category_data': category_amount,
        'termini_labels': termini_name,
        'termini_data': termini_amount,
        'out_in_labels': out_in_labels,
        'out_in_data': out_in_data,





    })


