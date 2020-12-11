from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import generic
from django.views.generic import DetailView, TemplateView, ListView
from accounts.models import *
from dashboard.models import *

# Dashboard view. LoginRequiredMixin redirects users to login page if they are not authenticated
class UserDashboardView(LoginRequiredMixin, DetailView):
    template_name = 'dashboard/dashboard.html'
    def get_object(self, queryset=None):
        print(self.request.user.id)

class TransactionView(ListView):
    model = Transaction
    context_object_name = 'transactions_list'  # your own name for the list as a template variable
    template_name = 'dashboard/transactions.html'  # Specify your own template name/location
    # slug_field = "emp_no"
    # slug_url_kwarg = "emp_no"
    #
    # # def get_object(self, queryset=None):
    # #     pk = self.request.user.id
    # #     queryset = Transaction.objects.filter(Customer_id=pk)
    # #     print(pk)
    # def get_queryset(self):
    #     return Transaction.objects.filter(Customer_id=self.request.user.id)







