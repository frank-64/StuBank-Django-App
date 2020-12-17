from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.generic import DetailView, TemplateView, ListView
from accounts.models import *
from dashboard.models import *
from django_otp.decorators import otp_required


#@method_decorator(otp_required, name='dispatch')
class UserDashboardView(DetailView):
    def get_object(self, queryset=None):
        if(self.request.user.is_customer):
            UserDashboardView.template_name = 'dashboard/customer_dashboard.html'
        else:
            UserDashboardView.template_name = 'dashboard/helper_dashboard.html'


#@method_decorator(otp_required, name='dispatch')
class TransactionListView(ListView):
    model = Transaction
    context_object_name = 'transaction_list'
    template_name = 'dashboard/transactions.html'


#@method_decorator(otp_required, name='dispatch')
class TransactionDetailView(DetailView):
    model = Transaction
    context_object_name = 'transaction_list'
    template_name = 'dashboard/transactions.html'
    slug_field = 'order_id'

    def get_queryset(self):
        return super(TransactionDetailView, self).get_queryset()

    def get_object(self):
        return self.get_queryset().filter(Customer_id=self.request.user.pk)


