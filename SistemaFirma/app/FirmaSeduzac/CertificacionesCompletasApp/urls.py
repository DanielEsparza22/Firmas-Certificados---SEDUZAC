from django.urls import path
from . import views

urlpatterns = [
    path('', views.certificaciones_completas, name="certificaciones_completas"),
    path('reiniciar_foliador/', views.reiniciar_foliador_cc, name="reiniciar_foliador_cc"),
    path('consultar_registros/', views.consultar_registros_no_firma_cc, name="consultar_registros_no_firma_cc"),

]