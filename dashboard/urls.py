from django.urls import path
from dashboard.views import *

urlpatterns = [
    path('', UserDashboardView.as_view(), name='dashboard'),
    path('transactions/', TransactionView.as_view(), name='transactions'),
    path('test/', testing, name='test')
    # path('livechat/', UserDashboardView.as_view(), name='dashboard'),
    # path('addpayee/', UserDashboardView.as_view(), name='dashboard'),
    # path('viewpayees/', UserDashboardView.as_view(), name='dashboard'),
]