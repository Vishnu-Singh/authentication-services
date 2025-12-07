from django.urls import path
from . import views

urlpatterns = [
    path('api-key/create/', views.create_api_key, name='create_api_key'),
    path('api-key/list/', views.list_api_keys, name='list_api_keys'),
    path('api-key/<int:key_id>/revoke/', views.revoke_api_key, name='revoke_api_key'),
    path('api-key/verify/', views.verify_api_key, name='verify_api_key'),
    path('hmac/verify/', views.verify_hmac, name='verify_hmac'),
    path('basic/', views.basic_auth, name='basic_auth'),
]
