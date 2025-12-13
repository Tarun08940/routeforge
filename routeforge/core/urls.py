from django.urls import path
from .views import route_estimate, home

urlpatterns = [
    path("", home),
    path("api/route", route_estimate),
]
