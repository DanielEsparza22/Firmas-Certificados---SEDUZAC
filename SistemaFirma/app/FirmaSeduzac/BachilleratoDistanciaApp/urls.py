from django.urls import path
from . import views

urlpatterns = [
    path('', views.bachillerato_distancia, name="bachillerato_distancia"),
]