from django.shortcuts import redirect
from django.views.generic.edit import CreateView, FormView
from django.views.generic.base import TemplateView
from django_otp import devices_for_user
from django.contrib.auth import views as auth_views, authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django_otp.plugins.otp_totp.models import TOTPDevice
from .forms import UserRegisterForm, UserInputQrCodeForm
from django_otp.forms import OTPAuthenticationForm
from .models import User
import qrcode


def get_user_totp_device(self, user, confirmed=None):
    devices = devices_for_user(user, confirmed=confirmed)
    for device in devices:
        if isinstance(device, TOTPDevice):
            return device


def generate_qr(data, size, border):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=size, border=border)
    qr.add_data(data)
    qr.make(fit=True)
    return qr.make_image()


class CustomLoginView(auth_views.LoginView):
    template_name = 'accounts/login.html'
    form_class = OTPAuthenticationForm


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'accounts/register.html'
    success_url = '/totp/create'

    def form_valid(self, form):
        form.save()
        username = self.request.POST['username']
        password = self.request.POST['password1']

        user = authenticate(username=username, password=password)
        login(self.request, user)
        return redirect(self.success_url)



# Create TOTP QR code and ask for user code input
class TOTPCreateView(FormView):
    template_name = 'two_factor_auth/totp_create.html'
    form_class = UserInputQrCodeForm

    # Get the url which will be transformed into a QR code
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        device = get_user_totp_device(self, user)

        if not device:
            device = user.totpdevice_set.create(confirmed=False)
        url = device.config_url
        context['url'] = url
        return context

    # Redirect the user to their dashboard or the login page, depending on the success of the auth code
    def form_valid(self, form):
        code = form.cleaned_data.get('code')
        user = self.request.user
        device = get_user_totp_device(self, user)

        if not device is None and device.verify_token(code):
            if not device.confirmed:
                device.confirmed = True
                device.save()
            return redirect('dashboard_home')
        return redirect('login')
