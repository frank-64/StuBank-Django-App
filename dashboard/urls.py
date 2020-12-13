from django.conf.urls import url
from django.urls import path
from dashboard.views import *

urlpatterns = [
    path('', UserDashboardView.as_view(), name='dashboard_home'),
    path('viewpayees/', PayeeDetailView.as_view(), name='viewpayee'),
    # path('livechat/', UserDashboardView.as_view(), name='livechat'),
    # path('addpayee/', UserDashboardView.as_view(), name='addpayee'),


    # path('transactions/all/', TransactionListView.as_view(), name='transactions'),
    # path('transactions/detail/', TransactionDetailView.as_view(), name='transactions_user'),
]