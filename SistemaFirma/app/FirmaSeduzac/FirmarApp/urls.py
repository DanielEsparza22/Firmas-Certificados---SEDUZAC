from django.urls import path
from . import views

urlpatterns = [
    path('', views.firmar, name="firmar"),
]