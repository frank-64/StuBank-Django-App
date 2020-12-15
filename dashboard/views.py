from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import DetailView, TemplateView, ListView, CreateView
from django.views.generic.base import View
from .forms import *
from dashboard.models import *

# Dashboard view. LoginRequiredMixin redirects users to login page if they are not authenticated
class UserDashboardView(LoginRequiredMixin, DetailView):
    model = Transaction
    context_object_name = 'transaction_list'
    def get_object(self, queryset=None):
        if(self.request.user.is_customer):
            UserDashboardView.template_name = 'dashboard/customer/customer_dashboard.html'
            return self.get_queryset().filter(Customer_id=self.request.user.pk)
        else:
            UserDashboardView.template_name = 'dashboard/helper/helper_dashboard.html'

    def get_queryset(self):
        return super(UserDashboardView, self).get_queryset()

class PayeeDetailView(DetailView):
    model = Payee
    context_object_name = 'payee_list'
    template_name = 'dashboard/customer/payee_dashboard.html'


    def get_queryset(self):
        return super(PayeeDetailView, self).get_queryset()

    def get_object(self):
        return self.get_queryset().filter(User_id=self.request.user.pk)

def delete_payee(request, pk):
    Payee.objects.filter(pk=pk).delete()
    response = redirect('/dashboard/viewpayees/')
    return response

def add_payee(request):
    # if this is a POST request we need to process the form data
    form = PayeeDetailsForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        sort_code = form.cleaned_data['sort_code']
        account_num = form.cleaned_data['account_num']
        try:
            payee_object = Customer.objects.filter(sort_code=sort_code, account_num=account_num,
                                                   user__first_name=first_name, user__last_name=last_name)
            payee_id = payee_object[0].pk
            user_id = request.user.pk
            p = Payee(PayeeID_id=payee_id, User_id=user_id)
            p.save()
            return redirect('/dashboard/viewpayees/')
        except:
            error_title = 'Could not add payee!'
            resolution = 'Did you enter the correct details? Sort code should be in the form DD-DD-DD with hyphens included.'
            return render(request, 'dashboard/customer/error.html', {'error_title': error_title, 'resolution': resolution})

    return render(request, 'dashboard/customer/add_payee.html', {'form': form})


def payee_transfer(request):
    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = TransferForm(request.user, data=request.POST)

        # Check if the form is valid:
        if form.is_valid:

            return HttpResponse('Thanks')
            #return HttpResponseRedirect(reverse('all-borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        form = TransferForm(request.user)

    context = {
        'form': form,
    }

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




