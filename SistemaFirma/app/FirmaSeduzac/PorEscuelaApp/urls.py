from django.urls import path
from . import views

urlpatterns = [
    path('', views.por_escuela, name="por_escuela"),
    path('reiniciar_foliador/', views.reiniciar_foliador_pe, name="reiniciar_foliador_pe"),
]