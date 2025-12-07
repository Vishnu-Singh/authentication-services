from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.session_login, name="session_login"),
    path("logout/", views.session_logout, name="session_logout"),
    path("status/", views.session_status, name="session_status"),
    path("register/", views.register, name="register"),
]
