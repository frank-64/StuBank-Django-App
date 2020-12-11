from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views import generic
from django.views.generic import DetailView, TemplateView, ListView
from accounts.models import *
from dashboard.models import *

# Dashboard view. LoginRequiredMixin redirects users to login page if they are not authenticated
class UserDashboardView(LoginRequiredMixin, DetailView):
    template_name = 'dashboard/dashboard.html'
    def get_object(self, queryset=None):
        pass

class TransactionListView(ListView):
    model = Transaction
    context_object_name = 'transaction_list'
    template_name = 'dashboard/transactions.html'


class TransactionDetailView(DetailView):
    model = Transaction
    context_object_name = 'transaction_list'
    template_name = 'dashboard/transactions.html'
    slug_field = 'order_id'


    def get_queryset(self):
        return super(TransactionDetailView, self).get_queryset()

    def get_object(self):
        return self.get_queryset().filter(Customer_id=self.request.user.pk)




