from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Transaction)
admin.site.register(Payee)
admin.site.register(Card)