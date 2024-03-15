from django.urls import path
from . import views

urlpatterns = [
    path('', views.certificaciones_completas, name="certificaciones_completas"),
]