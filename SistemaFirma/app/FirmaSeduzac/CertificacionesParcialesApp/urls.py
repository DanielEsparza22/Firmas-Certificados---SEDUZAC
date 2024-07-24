from django.urls import path
from . import views

urlpatterns = [
    path('', views.certificaciones_parciales, name="certificaciones_parciales"),
    # path('reiniciar_foliador/', views.reiniciar_foliador_cp, name="reiniciar_foliador_cp"),
    path('consultar_registros_no_firma_cp/', views.consultar_registros_no_firma_cp, name="consultar_registros_no_firma_cp"),
    path('consultar_registros_cp/', views.consultar_registros_firmados_cp, name="consultar_registros_cp"),
    path('generar_pdf_cp/<str:curp>', views.generar_pdf_cp, name="generar_pdf_cp"),

]