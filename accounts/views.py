from django.conf import settings
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Q
from django.http import BadHeaderError, HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
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
    """
        Written by: Ed
        Purpose: Retrieve all TOTP devices registered with the user
    """

    devices = devices_for_user(user, confirmed=confirmed)
    for device in devices:
        if isinstance(device, TOTPDevice):
            return device


def generate_qr(data, size, border):
    """
        Written by: Ed
        Purpose: Generate a .png QR code image file from the 'data' parameter. To be used for verifying a TOTP device
    """

    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=size, border=border)
    qr.add_data(data)
    qr.make(fit=True)
    return qr.make_image()


class CustomTOTPLoginView(auth_views.LoginView):
    """
        Written by: Ed
        Purpose: Custom login view displaying the CustomAuthenticationForm which allows for login using the TOTP
    """

    template_name = 'accounts/login.html'
    form_class = CustomAuthenticationForm

class infoView(auth_views.LoginView):
    template_name = 'accounts/info.html'
    #form_class = CustomAuthenticationForm


class RegisterView(CreateView):
    """
        Written by: Ed
        Purpose: Registration view page allowing user to register an account. Displays registration form and redirects
                user to TOTPCreateView
    """

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
    """
        Written by: Ed
        Purpose: Create QR code from the TOTP authentication link and display it to user to allow for confirmation of
                device and completion of the registration process.
    """

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

def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "StuBank Password Reset Requested"
                    email_template_name = "registration/password_reset_email.html"
                    c = {
                        "email": user.email,
                        'domain': 'stubank.tk',
                        'site_name': 'StuBank',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                        'protocol': 'https',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'AWS_verified_email_address', [user.email], fail_silently=False)
                    except BadHeaderError:

                        return HttpResponse('Invalid header found.')

                    messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
                    return redirect(reverse('password_reset_done'))
            messages.error(request, 'An invalid email has been entered.')
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="registration/password_reset_form.html",
                  context={"password_reset_form": password_reset_form})