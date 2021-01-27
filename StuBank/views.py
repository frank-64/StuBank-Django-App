from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponse, BadHeaderError
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views import View
from accounts.models import *
# Create your views here.

class Index(View):
    """
            Written by: Tom
            Purpose: Render the homepage html file
    """
    def index_page(request):
        return render(request, "StuBank/index.html")



def info_page(request):
    return render(request, "StuBank/info.html")
