from django.urls import path
from . import views

urlpatterns = [
    path('', views.por_escuela, name="por_escuela"),
]