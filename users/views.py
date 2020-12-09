from django.contrib.auth.views import LoginView, LogoutView, TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render


# Create your views here.

# Dashboard view. LoginRequiredMixin redirects users to login page if they are not authenticated
class UserDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'users/dashboard.html'


class RegisterView(TemplateView):
    template_name = 'users/register.html'
