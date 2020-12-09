from django.urls import path
from users.views import UserDashboardView, RegisterView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', UserDashboardView.as_view(), name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logged_out.html'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('passwordReset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset_form.html'), name='password_reset'),

]