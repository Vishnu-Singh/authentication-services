from django.urls import path
from . import views

urlpatterns = [
    path('magic-link/request/', views.request_magic_link, name='request_magic_link'),
    path('magic-link/verify/', views.verify_magic_link, name='verify_magic_link'),
    path('otp/request/', views.request_otp, name='request_otp'),
    path('otp/verify/', views.verify_otp, name='verify_otp'),
]
