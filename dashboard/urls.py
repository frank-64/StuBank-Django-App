from django.urls import path
from users.views import UserDashboardView
from dashboard.views import *

urlpatterns = [
    path('', UserDashboardView.as_view(), name='Dashboard Home'),
]