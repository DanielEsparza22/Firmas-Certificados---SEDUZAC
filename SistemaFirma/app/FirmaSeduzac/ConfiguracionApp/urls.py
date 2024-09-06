from django.urls import path
from . import views

urlpatterns = [
    path('reiniciar_foliador/', views.reiniciar_foliador, name="reiniciar_foliador"),
    path('actualizar_autoridad/', views.actualizar_autoridad_educativa, name="actualizar_autoridad"),
    path('catalogo_bachilleratos/', views.catalogo_bachilleratos, name="catalogo_bachilleratos"),
    path('catalogo_bachilleratos/agregar/', views.agregar_bachillerato, name="agregar_bachillerato"),
    path('catalogo_bachilleratos/editar/<int:id>', views.editar_bachillerato, name="editar_bachillerato"),
    path('catalogo_bachilleratos/eliminar/<int:id>', views.eliminar_bachillerato, name="eliminar_bachillerato"),
]