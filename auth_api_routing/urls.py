from django.urls import path
from . import views

urlpatterns = [
    path('forward/', views.route_request, name='route_request'),
    path('soap/', views.soap_endpoint, name='soap_endpoint'),
    path('list/', views.list_routes, name='list_routes'),
    path('create/', views.create_route, name='create_route'),
]
