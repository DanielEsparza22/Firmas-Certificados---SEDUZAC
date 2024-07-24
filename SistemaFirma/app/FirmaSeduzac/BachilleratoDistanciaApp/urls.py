from django.urls import path
from . import views

urlpatterns = [
    path('', views.bachillerato_distancia, name="bachillerato_distancia"),
    # path('reiniciar_foliador/', views.reiniciar_foliador_bd, name="reiniciar_foliador_bd"),
]