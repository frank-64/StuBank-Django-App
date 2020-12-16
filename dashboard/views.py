from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views import generic
from django.views.generic import DetailView, TemplateView, ListView
from accounts.models import *
from dashboard.models import *
from django_otp.decorators import otp_required


# Dashboard view. LoginRequiredMixin redirects users to login page if they are not authenticated
class UserDashboardView(DetailView):
    def get_object(self, queryset=None):
        if(self.request.user.is_customer):
            UserDashboardView.template_name = 'dashboard/customer_dashboard.html'
        else:
            UserDashboardView.template_name = 'dashboard/helper_dashboard.html'

    # Prevent non-2FA-verified users from accessing this page
    @otp_required
    def dispatch(self, request, *args, **kwargs):
        return super(UserDashboardView, self).dispatch(request, *args, **kwargs)

class TransactionListView(ListView):
    model = Transaction
    context_object_name = 'transaction_list'
    template_name = 'dashboard/transactions.html'

    # Prevent non-2FA-verified users from accessing this page
    @otp_required
    def dispatch(self, request, *args, **kwargs):
        return super(TransactionListView, self).dispatch(request, *args, **kwargs)


class TransactionDetailView(DetailView):
    model = Transaction
    context_object_name = 'transaction_list'
    template_name = 'dashboard/transactions.html'
    slug_field = 'order_id'


    def get_queryset(self):
        return super(TransactionDetailView, self).get_queryset()

    def get_object(self):
        return self.get_queryset().filter(Customer_id=self.request.user.pk)

    # Prevent non-2FA-verified users from accessing this page
    @otp_required
    def dispatch(self, request, *args, **kwargs):
        return super(TransactionDetailView, self).dispatch(request, *args, **kwargs)


