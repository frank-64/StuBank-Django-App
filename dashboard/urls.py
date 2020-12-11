from django.urls import path
from dashboard.views import *

urlpatterns = [
    path('', UserDashboardView.as_view(), name='dashboard'),
    path('transactions/', TransactionView.as_view(), name='transactions'),
    # path('livechat/', UserDashboardView.as_view(), name='livechat'),
    # path('addpayee/', UserDashboardView.as_view(), name='addpayee'),
    # path('viewpayees/', UserDashboardView.as_view(), name='viewpayee'),
]