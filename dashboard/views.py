from django.shortcuts import render

# Create your views here.
from django.views import View
from django.views.generic import DetailView


class UserDetailView(object):
    pass


class CurrentUserDetailView(DetailView):
    def get_object(self, queryset=None):
        print(self.request.pk)
        print(self.request.first_name)
        return self.request.pk
