from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, TemplateView
from accounts.models import User

# Dashboard view. LoginRequiredMixin redirects users to login page if they are not authenticated
class UserDashboardView(LoginRequiredMixin, TemplateView, DetailView):
    template_name = 'dashboard/dashboard.html'
    def get_context_data(self, **kwargs):
        print(self.request.user.id)
        user = User.objects.get(self.request.user.id)
        return user

