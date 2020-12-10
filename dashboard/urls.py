from django.urls import path
from accounts.views import UserDashboardView

urlpatterns = [
    path('', UserDashboardView.as_view(), name='Dashboard Home'),
]