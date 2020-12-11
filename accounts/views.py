from django.views.generic.edit import CreateView
from .forms import UserRegisterForm
from .models import User

class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'accounts/register.html'
    success_url = '/login/'