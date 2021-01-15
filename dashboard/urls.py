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
    path('freeze-card/', customer_card_frozen, name='card_frozen'),
    path('transaction/', card_transaction, name='transaction'),
    path('moneypots/', MoneyPotListView.as_view(), name='money_pots'),
    path('moneypots/create/', MoneyPotCreateView.as_view(), name='add_money_pot'),
    path('moneypots/<int:pk>/delete', MoneyPotDeleteView.as_view(), name='delete_money_pot'),
    path('moneypots/<int:pk>/update', MoneyPotUpdateView.as_view(), name='update_money_pot'),
    path('moneypots/<int:pk>/deposit', MoneyPotDepositView.as_view(), name='deposit_money_pot'),
    path('help/', help_page, name='help'),
    path('gethelper/', get_helper, name='gethelper'),
    path('statement/', pdf_view, name='statement'),
    path('overview/', expenditure_overview, name='overview'),
    path('livechat/<int:pk>/', livechat, name='livechat'),
    path('message/<int:pk>/', message, name='message'),
    path('helper/chatlist/', get_livechats, name='helper_livechat'),
    path('livechat/helper-perms/<int:pk>/', grant_permission, name='helper_perms'),
    path('livechat/deactivate/<int:pk>/', deactivate_livechat, name='deactivate_livechat'),
    path('livechat/freeze-account/<int:pk>/', toggle_account_frozen, name='toggle_account'),
    path('livechat/freeze-card/<int:pk>/', toggle_card_frozen, name='freeze_card'),
    path('livechat/transactions/<int:pk>/', LiveChatTransactions.as_view(), name='cust_transactions')
]