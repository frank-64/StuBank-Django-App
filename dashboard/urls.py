from django.urls import path
from accounts.views import UserDashboardView
from dashboard.views import *

urlpatterns = [
    path('', UserDashboardView.as_view(), name='dashboard'),
    path('home', AccountInfoView.as_view(), name='dashboard'),
]