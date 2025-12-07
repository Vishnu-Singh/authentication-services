from django.urls import path
from . import views

urlpatterns = [
    path('authorize/', views.oauth_authorize, name='oauth_authorize'),
    path('token/', views.oauth_token, name='oauth_token'),
    path('userinfo/', views.oauth_userinfo, name='oauth_userinfo'),
    path('.well-known/openid-configuration/', views.oidc_discovery, name='oidc_discovery'),
    path('social/', views.social_login, name='social_login'),
]
