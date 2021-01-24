from django.urls import path
from FakeTransactions import views

urlpatterns = [
    path('transaction/', views.AddNewTransaction, name="StuShop"),
    path('', views.StuShopRender, name="StuShop")
]