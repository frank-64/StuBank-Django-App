from django.urls import path
from StuBank.views import *

urlpatterns = [
    path('', Index.as_view, name="index"),
    path('info/', info_page, name='info'),
]