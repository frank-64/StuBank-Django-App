from django.urls import path
from users.views import UserDashboardView

urlpatterns = [
    path('', UserDashboardView.as_view(), name='Dashboard Home'),
]