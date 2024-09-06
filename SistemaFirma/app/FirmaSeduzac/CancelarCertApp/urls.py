from django.urls import path
from . import views

urlpatterns = [
    path('', views.cancelar_certificado, name="cancelar_certificado"),
]