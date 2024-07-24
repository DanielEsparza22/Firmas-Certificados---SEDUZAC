from django.urls import path
from . import views

urlpatterns = [
    path('reiniciar_foliador/', views.reiniciar_foliador, name="reiniciar_foliador"),
    path('actualizar_autoridad/', views.actualizar_autoridad_educativa, name="actualizar_autoridad"),
]