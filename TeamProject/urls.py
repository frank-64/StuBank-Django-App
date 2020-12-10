from django.contrib import admin
from django.urls import path, include
from StuBank import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('StuBank.urls')),
    path('', include('users.urls')),
    path('dashboard/', include('dashboard.urls')),
]
