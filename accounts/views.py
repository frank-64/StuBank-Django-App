from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from django.views.generic.edit import CreateView, FormView
from django_otp import devices_for_user
from django.contrib.auth import views as auth_views, authenticate, login, logout
from django_otp.decorators import otp_required
from django_otp.plugins.otp_totp.models import TOTPDevice
from .forms import UserRegisterForm, UserInputQrCodeForm, CustomAuthenticationForm
from django_otp.forms import OTPAuthenticationForm
from .models import User, Customer
import qrcode
from django.core.files.base import ContentFile, File


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


class CustomTOTPLoginView(auth_views.LoginView):
    template_name = 'accounts/login.html'
    form_class = CustomAuthenticationForm


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
    model = Customer
    template_name = 'two_factor_auth/totp_create.html'
    form_class = UserInputQrCodeForm

    # Get the url which will be transformed into a QR code
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # If there isn't a device registered with this user, then create a new device
        device = get_user_totp_device(self, user)
        if not device:
            device = user.totpdevice_set.create(confirmed=False)

        # Retrieve the url for the QR code and the current customer from the database
        url = device.config_url
        customer = Customer.objects.get(user=user)

        # If no QR code has been generated for this user before, then generate one
        if not customer.qrcode_generated:
            filepath = user.username + '.png'
            qr_file = ContentFile(b'', name=filepath)
            qrcode.make(url).save(qr_file, format='PNG')
            customer.qrcode_file = qr_file
            customer.qrcode_generated = True
            customer.save()

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
        return redirect('totp_create')

