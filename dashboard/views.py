from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from django.views.generic import DetailView


class AccountInfoView(DetailView):
    template_name = 'dashboard/dashboard.html'
    def get_object(self, queryset=None):
        print(self.request.user.pk)
        print(self.request.user.username)
