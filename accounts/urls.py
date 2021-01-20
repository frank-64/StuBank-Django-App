from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import RegisterView, TOTPCreateView, CustomTOTPLoginView
from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = [
    path('login/', CustomTOTPLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(template_name='accounts/logged_out.html'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('passwordReset/', PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    path('totp/create', TOTPCreateView.as_view(), name='totp_create'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)