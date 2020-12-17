from django.urls import path
from FakeTransactions import views

urlpatterns = [
    path('', views.FakeTransactions.AddNewTransaction, name="faketransactions")
]