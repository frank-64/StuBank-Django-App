from django.conf.urls import url
from django.urls import path
from dashboard.views import *

urlpatterns = [
    path('', UserDashboardView.as_view(), name='dashboard_home'),
    path('viewpayees/', PayeeDetailView.as_view(), name='viewpayee'),
    path('removepayee/<int:pk>/', delete_payee, name='removepayee'),
    path('addpayee/', add_payee, name='addpayee'),
    path('transfer/', payee_transfer, name='transfer'),
    path('moneypots/', MoneyPotListView.as_view(), name='money_pots'),
    path('moneypots/create/', MoneyPotCreateView.as_view(), name='add_money_pot'),
    path('moneypots/<int:pk>/delete', MoneyPotDeleteView.as_view(), name='delete_money_pot'),
    path('moneypots/<int:pk>/update', MoneyPotUpdateView.as_view(), name='update_money_pot'),
    # path('transfer/get-payees', payee_list, name='get-payees')
    # path('livechat/', UserDashboardView.as_view(), name='livechat'),
    # path('transactions/all/', TransactionListView.as_view(), name='transactions'),
    # path('transactions/detail/', TransactionDetailView.as_view(), name='transactions_user'),
]