from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views import generic
from django.views.generic import DetailView, TemplateView, ListView
from accounts.models import *
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




