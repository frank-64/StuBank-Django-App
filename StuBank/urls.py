from django.urls import path
from StuBank import views

urlpatterns = [
    path('', views.Index.index_page, name="index")
]