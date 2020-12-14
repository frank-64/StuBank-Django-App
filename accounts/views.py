from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django_otp import devices_for_user
from django_otp.plugins.otp_totp.models import TOTPDevice
from .forms import UserRegisterForm
from .models import User


def get_user_totp_device(self, user, confirmed=None):
    devices = devices_for_user(user, confirmed=confirmed)
    for device in devices:
        if isinstance(device, TOTPDevice):
            return device


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'accounts/register.html'
    success_url = '/login/'


# View to set up a new TOTP device
class TOTPCreateView(TemplateView):
    template_name = 'two_factor_auth/totp_create.html'

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        device = get_user_totp_device(self, user)

        if not device:
            device = user.totpdevice_set.create(confirmed=False)
        url = device.config_url
        context['url'] = url
        return context


# View to verify user
class TOTPVerifyView(TemplateView):

    def post(self, request, token):
        user = request.user
        device = get_user_totp_device(self, user)
        if not device == None and device.verify_token(token):
            if not device.confirmed:
                device.confirmed = True
                device.save()
            return True
        return False
