from django.urls import path
from StuBank.views import *

urlpatterns = [
    path('', Index.as_view, name="index"),
    path('password_reset', password_reset_request, name="password_reset")
]