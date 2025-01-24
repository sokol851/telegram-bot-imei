from django.urls import path

from .views import CheckIMEIView

urlpatterns = [
    path('check-imei/', CheckIMEIView.as_view(), name='check-imei'),
]
