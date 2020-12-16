from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from decimal import Decimal
from django.views.generic import DetailView, TemplateView, ListView, CreateView
from django.views.generic.base import View
from .forms import *
from dashboard.models import *

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
    context_object_name = 'transaction_list'

    def get_queryset(self):
        """gets all the transactions as we set the view 'model = Transaction'

        :return: all transactions
        """
        return super(UserDashboardView, self).get_queryset()

    def get_object(self, queryset=None):
        """ checks if the current user is a helper or customer and sets the template_name accordingly

        :param request: HttpRequest object containing metadata and current user attributes
        :return: queryset of customer's transactions
        """
        if(self.request.user.is_customer):
            UserDashboardView.template_name = 'dashboard/customer/customer_dashboard.html'
            # queryset is set to that specific customer's transaction objects
            return self.get_queryset().filter(Customer_id=self.request.user.pk)
        else:
            UserDashboardView.template_name = 'dashboard/helper/helper_dashboard.html'


class PayeeDetailView(DetailView):
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


def delete_payee(request, pk):
    """deletes a payee

    :param request: HttpRequest object containing metadata and current user attributes
    :param pk: primary key in the payee table used to identify a specific row
    :return response: HttpResponse object which redirects to new url path
    """
    Payee.objects.filter(pk=pk).delete()
    response = redirect(reverse('viewpayee'))
    return response


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
            # TODO: Separate this to a separate method which uses AJAX to check if customer exists.
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
            return render(request, 'dashboard/customer/error.html', {'error_title': error_title, 'resolution': resolution})

    # if the request is not POST then render a response with the form on the add_payee.html page
    return render(request, 'dashboard/customer/add_payee.html', {'form': form})


def alter_balance(customers_customer_id, payees_customer_id, amount):
    """ changes the balance of the sender/customer and the reciever/payee

    :param customers_customer_id: primary key of the customer sending the money
    :param payees_customer_id: primary key of the payee receiving the money
    :param amount: how much to change the balances by
    :return:
    """
    # reduce customer's balance
    # get the customer's customer object using their primary key
    customer = Customer.objects.filter(pk=customers_customer_id)

    # cust_balance is the current balance of the customer
    cust_balance = customer[0].balance

    # cust_new_balance is the balance of the customer after removing the amount they are transferring
    cust_new_balance = cust_balance - amount

    # persisting the changed balance in the database
    Customer.objects.filter(pk=customers_customer_id).update(balance=cust_new_balance)


    # increase payee's balance
    # get the payees's customer object using their primary key
    payee = Customer.objects.filter(pk=payees_customer_id)

    # payee_balance is the current balance of the payee
    payee_balance = payee[0].balance

    # payee_new_balance is the balance of the customer after adding the amount they are receiving
    payee_new_balance = payee_balance + amount

    #persisting the changed balance in the database
    Customer.objects.filter(pk=payees_customer_id).update(balance=payee_new_balance)


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

            direction = 'OUT'

            # setting the transaction_time to the current time
            transaction_time = timezone.now()

            # getting the comment data from the form
            comment = form.data['Comment']

            # setting the new_balance to be the customer's balance after this transaction
            new_balance = request.user.customer.balance - amount

            # Termini is the main attribute to view in a transaction e.g. who you transferred the
            # money to/received the money from
            termini = payee_fname+" "+payee_lname

            # getting the category data from the form
            category = form.data['Category']

            # default method is Bank Transfer
            method = 'Bank Transfer'

            # creating the transaction object with all the above variables inserted into their matching fields
            transaction = Transaction(Payee_id=payee_id, Customer_id=customers_customer_id, Amount=amount,
                                      Direction=direction, TransactionTime=transaction_time, Comment=comment,
                                      NewBalance=new_balance, Termini=termini, Category=category,
                                      Method=method)
            try:
                # TODO: Transactions must be added on the other end so payees can see a transaction coming in from the customer
                if (amount < 1.00):
                    raise
                # persisting the transaction object
                transaction.save()

                # changing the balance for both the customer and payee
                alter_balance(customers_customer_id, payees_customer_id, amount)

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




