from django.conf.urls import url
from django.urls import path
from dashboard.views import *

urlpatterns = [
    path('', UserDashboardView.as_view(), name='dashboard_home'),
    path('viewpayees/', PayeeDetailView.as_view(), name='viewpayee'),
    path('removepayee/<int:pk>/', delete_payee, name='removepayee'),
    path('addpayee/', add_payee, name='addpayee'),
    path('transfer/', payee_transfer, name='transfer'),
    path('checkpayee/', check_payee, name='checkpayee'),
    path('getcard/', get_card, name='getcard'),
    path('transaction/', card_transaction, name='transaction'),
    path('moneypots/', MoneyPotListView.as_view(), name='money_pots'),
    path('moneypots/create/', MoneyPotCreateView.as_view(), name='add_money_pot'),
    path('moneypots/<int:pk>/delete', MoneyPotDeleteView.as_view(), name='delete_money_pot'),
    path('moneypots/<int:pk>/update', MoneyPotUpdateView.as_view(), name='update_money_pot'),
    path('moneypots/<int:pk>/deposit', MoneyPotDepositView.as_view(), name='deposit_money_pot'),
    path('livechat/<int:pk>/', livechat, name='livechat'),
    path('message/<int:pk>/', message, name='message')
]