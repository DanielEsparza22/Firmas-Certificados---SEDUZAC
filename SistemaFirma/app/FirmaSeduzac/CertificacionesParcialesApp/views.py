from django.shortcuts import render, redirect
import os
from django.http import HttpResponse
from .forms import CURPForm, RegistrosParcialesForm, FormFiltroCertificadosP
from django.contrib.auth.decorators import login_required
from .utils import test_consulta_datos
from django.db import connection, connections
from .utils import api_firma, fecha_a_texto, numero_a_texto
from datetime import datetime
import json
from FirmaSeduzac.settings import LETRA_FOLIO_TB, LETRA_FOLIO_BACHILLERATO_DISTANCIA
from ConfiguracionApp.models import FolioSequence, FolioLetra
from django.contrib import messages
from ConfiguracionApp.models import AutoridadEducativa
from .pdf_parcial import pdf_parciales

def verificar_certificado(cursor, curp):
    query = "SELECT * FROM alumno_cert_parcial WHERE curp = %s"
    cursor.execute(query, [curp])
    result = cursor.fetchone()
    if result:
        return dict(zip(['id_hist_estudio', 'curp', 'id_proceso', 'certificado_digital', 
                         'estatus_foto', 'estatus_certificado', 'fecha_creacion', 
                         'fecha_firma', 'sello_sep', 'fecha_sello_sep', 'folio_sep', 
                         'id_genero_ct', 'nombre_ct', 'clavecct', 'nivel_ct', 
                         'prim_apellido', 'seg_apellido', 'nombre', 'promedio', 
                         'fecha_cert', 'fecha_cert_texto', 'tipo_cert', 'entidad', 
                         'cv_mun', 'nom_mun', 'observaciones_tec', 'sello_seduzac', 
                         'fecha_certificacion', 'bachillerato', 'semestre', 
                         'autoridad_educativa', 'certificado_autoridad_educativa'], result))
    else:
        return None

def obtener_datos_alumno(cursor, curp):
    query = ("SELECT a.cve_alumno, a.curp, a.app_alumno, a.apm_alumno, "
             "a.nom_alumno, a.semestre, eb.clave_ct, a.alumno_estatus "
             "FROM alumnos a "
             "INNER JOIN escuela_bachillerato eb ON eb.cve_bach_ct = a.cve_bach_ct "
             "WHERE a.curp = %s;")
    cursor.execute(query, [curp])
    clave = cursor.fetchone()
    if clave:
        return dict(zip(['cve_alumno', 'curp', 'app_alumno', 'apm_alumno', 
                         'nom_alumno', 'semestre', 'clave_ct', 'alumno_estatus'], clave))
    else:
        return None
    
def obtener_clave_alumno(cursor, curp):
    query = ("SELECT cve_alumno FROM alumnos WHERE curp = %s;")
    cursor.execute(query, [curp])
    clave = cursor.fetchone()
    if clave:
        # print(f'CLAVE:{clave}')
        return clave
    else:
        return None

def obtener_registros_insertar(cursor, clave, fecha_cert, fecha_certificacion, bachillerato, semestre, nombre_autoridad, certificado_autoridad):
    query = (
        "SELECT a.cve_alumno AS id_hist_estudio, "
        "a.curp, 0 AS id_proceso, NULL AS certificado_digital, 0 AS estatus_foto, 0 AS estatus_certificado, "
        "CURDATE() AS fecha_creacion, NULL AS fecha_firma, NULL AS sello_sep ,NULL AS fecha_sello_sep, NULL AS folio_sep, "
        "s.id_genero_ct, s.nombre AS nombre_ct, e.clave_ct, NULL AS nivel_ct, TRIM(REPLACE(a.app_alumno, CHAR(9), ' ')) AS prim_apellido, "
        "TRIM(REPLACE(a.apm_alumno, CHAR(9), ' ')) AS seg_apellido, TRIM(REPLACE(a.nom_alumno, CHAR(9), ' ')) AS nombre, a.promedio, "
        "%s AS fecha_cert, NULL AS fecha_cert_texto, 3 AS tipo_cert, 32 AS entidad, '000' AS cve_mun, s.municipio AS nom_municipio, "
        "NULL AS observaciones_tec, NULL AS sello_seduzac, %s AS fecha_certificacion, %s AS bachillerato, %s AS semestre, "
        "%s AS autoridad_educativa, %s AS certificado_autoridad_educativa "
        "FROM alumnos a "
        "JOIN escuela_bachillerato e ON e.cve_bach_ct = a.cve_bach_ct "
        "JOIN escuelas s ON s.clave_ct = e.clave_ct "
        "WHERE a.cve_alumno = %s "
        "AND a.alumno_estatus IN ('R', 'N', 'P', 'B', 'I', 'D');"
    )
    cursor.execute(query, (fecha_cert, fecha_certificacion, bachillerato, semestre, nombre_autoridad, certificado_autoridad, clave))
    columnas = [col[0] for col in cursor.description]
    resultados = cursor.fetchall()
    return [dict(zip(columnas, fila)) for fila in resultados]

def insertar_registros(cursor, registros):
    for registro in registros:
        query = (
            "INSERT INTO alumno_cert_parcial (id_hist_estudio, curp, id_proceso, certificado_digital, estatus_foto, estatus_certificado, "
                "fecha_creacion, fecha_firma, sello_sep, fecha_sello_sep, folio_sep, id_genero_ct, nombre_ct, clavecct, nivel_ct, prim_apellido, "
                "seg_apellido, nombre, promedio, fecha_cert, fecha_cert_texto, tipo_cert, entidad, cv_mun, nom_mun, observaciones_tec, "
                "sello_seduzac, fecha_certificacion, bachillerato, semestre, autoridad_educativa, certificado_autoridad_educativa) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        )
        cursor.execute(query, (
                registro['id_hist_estudio'], registro['curp'], registro['id_proceso'], registro['certificado_digital'],
                registro['estatus_foto'], registro['estatus_certificado'], registro['fecha_creacion'], registro['fecha_firma'],
                registro['sello_sep'], registro['fecha_sello_sep'], registro['folio_sep'], registro['id_genero_ct'], 
                registro['nombre_ct'], registro['clave_ct'], registro['nivel_ct'], registro['prim_apellido'], registro['seg_apellido'],
                registro['nombre'], registro['promedio'], registro['fecha_cert'], registro['fecha_cert_texto'], registro['tipo_cert'], 
                registro['entidad'], registro['cve_mun'], registro['nom_municipio'], registro['observaciones_tec'], 
                registro['sello_seduzac'], registro['fecha_certificacion'], registro['bachillerato'], registro['semestre'], 
                registro['autoridad_educativa'], registro['certificado_autoridad_educativa']
            ))
        
def obtener_valores_cadena(cursor, curp):
    rfc = "SAFC7105149R3"
    documento = "certificado"
    sistema = "certificacion"
    cadena = ""

    query = (
        "SELECT a.curp, a.nom_alumno, a.app_alumno, a.apm_alumno, a.promedio, s.clave_ct FROM alumnos a "
        "JOIN escuela_bachillerato s ON s.cve_bach_ct = a.cve_bach_ct "
        "WHERE a.curp = %s"
    )

    cursor.execute(query, [curp])
    alumno = cursor.fetchone()

    if(alumno):
        curp_alumno = alumno[0]
        nombre = alumno[1]
        ap_paterno = alumno[2]
        ap_materno = alumno[3]
        promedio = alumno[4]
        clavecct = alumno[5]
        fecha = datetime.now()
        fecha_final = fecha.strftime('%Y-%m-%d %H:%M:%S')

    print(alumno)

    cadena = f"||1.0|3|SAFC710514MDFLLR06|Secretaria de Educación|SECRETARÍA DE EDUCACIÓN DEL ESTADO DE ZACATECAS|Secretaría de Educación del Estado de Zacatecas|{clavecct}|000|32|{curp_alumno}|{nombre}|{ap_paterno}|{ap_materno}|3|{promedio}|{fecha_final}||"
    # print(cadena)
    firma = api_firma(rfc, documento, sistema, cadena)
    respuesta_json = json.loads(firma)
    sello = respuesta_json["sello"]
    uuid = respuesta_json["uuid"]
    fecha_firma = respuesta_json["fecha"]
    # print(f'SELLO : {sello}')
    # print(f'UUID : {uuid}')
    # print(f'FECHA : {fecha_firma}')

    valores_cadena = {'sello':sello, 'uuid':uuid, 'fecha':fecha_firma}

    return valores_cadena

def fecha_cert_texto(valores_cadena):
    fecha_texto = valores_cadena['fecha']
    fecha_res = fecha_a_texto(fecha_texto)

    return fecha_res

def firmar_certificado(cursor, curp, valores_cadena):
    id_proceso = 11111
    certificado_digital = ""
    estatus = 1
    fecha_firma = valores_cadena['fecha']
    fecha_texto = fecha_cert_texto(valores_cadena)
    sello = valores_cadena['sello']

    query = (
        "UPDATE alumno_cert_parcial SET id_proceso = %s, certificado_digital = %s, estatus_certificado = %s, "
        "fecha_firma = %s, fecha_cert_texto = %s, sello_seduzac = %s WHERE curp = %s"
    )
    cursor.execute(query, [id_proceso, certificado_digital, estatus, fecha_firma, fecha_texto, sello, curp])

def obtener_clave_cct(cursor,curp):
    query = (
        "SELECT ac.clavecct FROM alumno_cert_parcial ac WHERE ac.curp = %s"
    )
    cursor.execute(query,[curp])
    clavecct = cursor.fetchone()
    clavecct = clavecct[0]
    
    # print(f'LETRA: {LETRA_FOLIO}')
    return clavecct

def foliar_certificado_prepas(cursor, clavecct, curp, nombre_ct):
    try:
        foliador_prepa = FolioLetra.objects.latest('id')
    except:
        foliador_prepa = 'A'

    clave = clavecct[2:5]
    foliador = None
    if((clave == 'EBH' or clave == 'PBH') and nombre_ct != 'BACHILLERATO A DISTANCIA'):
        foliador = foliador_prepa
    elif(clave == 'ETK'):
        foliador = LETRA_FOLIO_TB
    elif(clave == 'EBH' and nombre_ct == 'BACHILLERATO A DISTANCIA'):
        foliador = LETRA_FOLIO_BACHILLERATO_DISTANCIA

    folio_sequence = FolioSequence.objects.create()
    folio_id = folio_sequence.id

    folio = f'{foliador}{str(folio_id).zfill(4)}'

    query = (
        "UPDATE alumno_cert_parcial SET folio_sep = %s WHERE curp = %s"
    )

    cursor.execute(query,[folio,curp])
    # print(f'FOLIADOR: {foliador}')

def datos_foliar(cursor, curp):
    query = (
        "SELECT * FROM alumno_cert_parcial WHERE curp = %s"
    )

    cursor.execute(query,[curp])
    registros_folio = cursor.fetchone()

    # print(registros_folio)
    return registros_folio

@login_required
def certificaciones_parciales(request):
    alumno_info = None
    error = None
    error_clave = None
    clave_info = None
    registros_insertar = None
    error_registros_insertar = None
    mensaje_insercion = None
    form_curp = CURPForm(request.POST or None)
    form_registros = RegistrosParcialesForm(request.POST or None)
    boton_enviar_datos = True
    curp = None
    datos_alumno = None
    seccion_datos = None
    seccion_guardar = None

    if(request.method == "POST"):
        with connections['mariadb'].cursor() as cursor:
            if(form_curp.is_valid()):
                curp = form_curp.cleaned_data['curp'].upper()
                request.session['curp'] = curp #Aqui guardo la curp en la sesion
                alumno_info = verificar_certificado(cursor, curp)
                datos_alumno = obtener_datos_alumno(cursor, curp)

                if(not alumno_info):
                    error = "No se encontró el certificado"
                    seccion_datos = True
                    seccion_guardar = True
                else:
                    seccion_datos = False
                    seccion_guardar = False
                if(not clave_info):
                    error_clave = "No se encontró la clave del alumno"

            if(form_registros.is_valid()):
                curp = request.session.get('curp', None) #Recupero la curp de la sesion
                clave = obtener_clave_alumno(cursor,curp)
                fecha_cert = form_registros.cleaned_data['fecha_certificacion']
                fecha_certificacion = form_registros.cleaned_data['fecha_certificacion']
                bachillerato = form_registros.cleaned_data['bachillerato'].upper() or "BACHILLERATO GENERAL"
                semestre = form_registros.cleaned_data['semestre']
                autoridad = AutoridadEducativa.objects.latest('id')
                nombre_autoridad = autoridad.nombre_autoridad
                certificado_autoridad = autoridad.certificado_autoridad
                resultados = obtener_registros_insertar(cursor, clave, fecha_cert, fecha_certificacion, bachillerato, semestre, nombre_autoridad, certificado_autoridad)

                if('obtener_registros' in request.POST):
                    if resultados:
                        registros_insertar = resultados
                        insertar_registros(cursor, resultados)
                        mensaje_insercion = "Datos guardados correctamente."
                        boton_enviar_datos = False
                    else:
                        error_registros_insertar = "No se encontraron registros para insertar."
                # elif('firmar' in request.POST):
                #     curp = request.session.get('curp', None) #Recupero la curp de la sesion
                #     if(curp):
                #         valores_cadena = obtener_valores_cadena(cursor, curp)
                #         # print(f'Valores de la cadena: {valores_cadena}')
                #         # print(fecha_cert_texto(valores_cadena))
                #         firmar_certificado(cursor, curp, valores_cadena)
                #         mensaje_firma = "Se firmó correctamente el certificado."
                #         seccion_foliador = True
                #         boton_enviar_datos = False
                #         datos_foliador = datos_foliar(cursor, curp)
                # elif('foliar' in request.POST):
                #     curp = request.session.get('curp', None) #Recupero la curp de la sesion
                #     if(curp):
                #         clave = obtener_clave_cct(cursor, curp)
                #         foliar_certificado_prepas(cursor, clave, curp)


    return render(request, 'cert_parc.html', {
        'form': form_curp,
        'form_registros': form_registros,
        'alumno_info': alumno_info,
        'error': error,
        'clave': clave_info,
        'error_clave': error_clave,
        'registros_info': registros_insertar,
        'error_registros_insertar': error_registros_insertar,
        'mensaje_insertar': mensaje_insercion,
        'boton_enviar':boton_enviar_datos,
        'datos_alumno':datos_alumno,
        'seccion_guardar':seccion_guardar,
        'seccion_datos':seccion_datos,
    })

# def reiniciar_foliador_cp(request):
#     mensaje = None
#     letra_form = LetraFoliadorForm(request.POST or None)
#     if(request.method == 'POST'):
#         if(letra_form.is_valid()):
#             letra_foliador = letra_form.cleaned_data['letra_foliador'].upper()
#             FolioLetraCP.objects.all().delete()
#             FolioLetraCP.objects.create(letra=letra_foliador)
#             reiniciar_secuencia_folio()
#             mensaje = f'Foliador restablecido: Letra nueva: {letra_foliador}, Secuencia restablecida a 1'

#     return render(request,"reiniciar_foliador_cp.html",{'letra_form':letra_form, 'mensaje':mensaje})

def registros_sin_firma(cursor):
    query = (
        "SELECT id_hist_estudio, curp, id_proceso, estatus_certificado, clavecct, prim_apellido, seg_apellido, nombre, promedio, "
        "sello_seduzac, folio_sep "
        "FROM alumno_cert_parcial WHERE estatus_certificado = 0;"
    )

    cursor.execute(query)
    registros = cursor.fetchall()

    # print(registros)
    return registros

# Obtener el nombre ct para foliar los bachilleratos a distancia
def obtener_nombre_ct(cursor, curp):
    query = ("SELECT nombre_ct FROM alumno_cert_parcial WHERE curp = %s;")

    cursor.execute(query,[curp])
    nombre_ct = cursor.fetchone()
    nombre_ct = nombre_ct[0]
    
    # print(f'LETRA: {LETRA_FOLIO}')
    return nombre_ct

@login_required
def consultar_registros_no_firma_cp(request):
    registros = None
    num_registros = 0
    with connections['mariadb'].cursor() as cursor:
        registros = registros_sin_firma(cursor)
        if (request.method == "POST"):
            registros_seleccionados = request.POST.getlist('select_registro')
            num_registros = len(registros_seleccionados)
            if(num_registros == 0):
                messages.error(request, f'Primero seleccione los registros a firmar y foliar')
            else:
                for registro_curp in registros_seleccionados:
                    valores_cadena = obtener_valores_cadena(cursor, registro_curp)
                    nombre_ct = obtener_nombre_ct(cursor, registro_curp)
                    firmar_certificado(cursor, registro_curp, valores_cadena)
                    clavecct = obtener_clave_cct(cursor,registro_curp)
                    foliar_certificado_prepas(cursor, clavecct, registro_curp, nombre_ct)

                messages.success(request, f'Se firmaron y foliaron {num_registros} registros exitosamente')
                return redirect('consultar_registros_no_firma_cp')
    return render(request,"consultar_registros_cp.html",{'registros':registros})

@login_required
def consultar_registros_firmados_cp(request):
    form_filtro = FormFiltroCertificadosP(request.POST or None)
    registros = None

    if request.method == "POST":
        if('reset_form' in request.POST):
            form_filtro = FormFiltroCertificadosP()
        else:
            with connections['mariadb'].cursor() as cursor:
                if(form_filtro.is_valid()):
                    curp = form_filtro.cleaned_data.get('curp')
                    fecha = form_filtro.cleaned_data.get('fecha_certificacion')
                    ct = form_filtro.cleaned_data.get('ct')

                    if(curp):
                        query2 = ("SELECT ac.curp, ac.bachillerato, ac.fecha_certificacion, ac.semestre, ac.clavecct FROM alumno_cert_parcial ac "
                                  "WHERE ac.curp = %s AND ac.estatus_certificado = 1")
                        cursor.execute(query2, [curp])
                        registros = cursor.fetchall()
                    elif(fecha):
                        query2 = ("SELECT ac.curp, ac.bachillerato, ac.fecha_certificacion, ac.semestre, ac.clavecct FROM alumno_cert_parcial ac "
                                  "WHERE ac.fecha_certificacion = %s AND ac.estatus_certificado = 1")
                        cursor.execute(query2, [fecha])
                        registros = cursor.fetchall()
                    elif(ct):
                        query2 = ("SELECT ac.curp, ac.bachillerato, ac.fecha_certificacion, ac.semestre, ac.clavecct FROM alumno_cert_parcial ac "
                                  "WHERE ac.clavecct = %s AND ac.estatus_certificado = 1")
                        cursor.execute(query2, [ct])
                        registros = cursor.fetchall()

    return render(request, "registros_firmados_cp.html", {'registros': registros, 'form_filtro': form_filtro})

def generar_pdf_cp(request, curp):
    pdf = pdf_parciales(curp)

    return pdf