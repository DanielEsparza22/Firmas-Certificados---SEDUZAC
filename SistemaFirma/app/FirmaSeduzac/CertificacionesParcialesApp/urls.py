from django.urls import path
from . import views

urlpatterns = [
    path('', views.certificaciones_parciales, name="certificaciones_parciales"),
    path('reiniciar_foliador/', views.reiniciar_foliador_cp, name="reiniciar_foliador_cp"),
]