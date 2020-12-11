from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import generic
from django.views.generic import DetailView, TemplateView
from accounts.models import *
from dashboard.models import *

# Dashboard view. LoginRequiredMixin redirects users to login page if they are not authenticated
class UserDashboardView(LoginRequiredMixin, DetailView):
    template_name = 'dashboard/dashboard.html'
    def get_object(self, queryset=None):
        print(self.request.user.id)

class TransactionView(generic.ListView):
    pk = None
    def get_object(self, queryset=None):
        pk = self.request.user.id
    model = Transaction
    context_object_name = 'transactions_list'   # your own name for the list as a template variable
    queryset = Transaction.objects.filter(Customer_id=pk)
    template_name = 'dashboard/transactions.html'  # Specify your own template name/location


def testing(request):
    return HttpResponse("Hello")



