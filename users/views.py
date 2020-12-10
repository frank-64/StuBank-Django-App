from django.contrib.auth.views import LoginView, LogoutView, TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from .forms import UserRegisterForm


# Create your views here.

# Dashboard view. LoginRequiredMixin redirects users to login page if they are not authenticated
class UserDashboardView(LoginRequiredMixin, TemplateView):
    # linking to Frankie's dashboard app
    template_name = 'dashboard/dashboard.html'


class RegisterView(CreateView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = '/login/'