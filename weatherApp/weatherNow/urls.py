from django.urls import path
from . import views

urlpatterns = [
    path('', views.weatherNow, name = 'weatherNow'),
]