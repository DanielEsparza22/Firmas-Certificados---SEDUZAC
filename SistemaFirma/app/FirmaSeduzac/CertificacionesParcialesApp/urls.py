from django.urls import path
from . import views

urlpatterns = [
    path('', views.certificaciones_parciales, name="certificaciones_parciales"),
]