
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
# Create your views here.

class Index(View):
    def index_page(request):
        return render(request, "StuBank/index.html")