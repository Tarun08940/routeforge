from django.urls import path
from .views import home, route_estimate, create_delivery

urlpatterns = [
    path("", home),
    path("api/route", route_estimate),
    path("api/deliveries", create_delivery),
]
