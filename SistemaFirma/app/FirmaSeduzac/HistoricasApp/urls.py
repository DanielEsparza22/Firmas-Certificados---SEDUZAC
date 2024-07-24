from django.urls import path
from . import views

urlpatterns = [
    path('', views.certificaciones_historicas, name="certificaciones_historicas"),
]