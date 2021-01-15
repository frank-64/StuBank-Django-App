from django.urls import path
from FakeTransactions import views

urlpatterns = [
    path('', views.AddNewTransaction, name="faketransactions")
]