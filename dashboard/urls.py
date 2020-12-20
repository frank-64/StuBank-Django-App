from django.conf.urls import url
from django.urls import path
from dashboard.views import *

urlpatterns = [
    path('', UserDashboardView.as_view(), name='dashboard_home'),
    path('viewpayees/', PayeeDetailView.as_view(), name='viewpayee'),
    path('removepayee/<int:pk>/', delete_payee, name='removepayee'),
    path('addpayee/', add_payee, name='addpayee'),
    path('transfer/', payee_transfer, name='transfer'),
    path('addmoneypot/', MoneyPotCreateView.as_view(), name='add_money_pot'),
    path('moneypots/', MoneyPotListView.as_view(), name='money_pots'),
    # path('transfer/get-payees', payee_list, name='get-payees')
    # path('livechat/', UserDashboardView.as_view(), name='livechat'),
    # path('transactions/all/', TransactionListView.as_view(), name='transactions'),
    # path('transactions/detail/', TransactionDetailView.as_view(), name='transactions_user'),
]