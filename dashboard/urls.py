from django.urls import path
from dashboard.views import *

urlpatterns = [
    path('', UserDashboardView.as_view(), name='dashboard_home'),
    path('viewpayees/', PayeeDetailView.as_view(), name='viewpayee'),
    path('removepayee/<int:pk>/', delete_payee, name='removepayee'),
    path('addpayee/', add_payee, name='addpayee'),
    # path('livechat/', UserDashboardView.as_view(), name='livechat'),
    # path('transactions/all/', TransactionListView.as_view(), name='transactions'),
    # path('transactions/detail/', TransactionDetailView.as_view(), name='transactions_user'),
]