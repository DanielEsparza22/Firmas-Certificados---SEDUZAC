from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import RegistrosPorEscuelaForm, LetraFoliadorForm
from django.db import connections
from .utils import api_firma, fecha_a_texto
from datetime import datetime
import json
from ConfiguracionApp.models import FolioLetra, FolioSequence
from FirmaSeduzac.settings import LETRA_FOLIO_TB
from ConfiguracionApp.models import AutoridadEducativa

def obtener_registros_insertar(cursor, clave, fecha_cert, fecha_certificacion, periodo, nombre_autoridad, certificado_autoridad):
    query = (
        "SELECT a.cve_alumno AS id_hist_estudio, "
        "a.curp, 0 AS id_proceso, NULL AS certificado_digital, 0 AS estatus_foto, 0 AS estatus_certificado, "
        "CURDATE() AS fecha_creacion, NULL AS fecha_firma, NULL AS sello_sep ,NULL AS fecha_sello_sep, NULL AS folio_sep, "
        "s.id_genero_ct, s.nombre AS nombre_ct, e.clave_ct, NULL AS nivel_ct, TRIM(REPLACE(a.app_alumno, CHAR(9), ' ')) AS prim_apellido, "
        "TRIM(REPLACE(a.apm_alumno, CHAR(9), ' ')) AS seg_apellido, TRIM(REPLACE(a.nom_alumno, CHAR(9), ' ')) AS nombre, a.promedio, "
        "%s AS fecha_cert, NULL AS fecha_cert_texto, 3 AS tipo_cert, 32 AS entidad, '000' AS cve_mun, s.municipio AS nom_municipio, "
        "NULL AS observaciones_tec, NULL AS sello_seduzac, %s AS fecha_certificacion, 'BACHILLERATO GENERAL' AS bachillerato, 'CERTIFICADO' AS certificacion, "
        "%s AS autoridad_educativa, %s AS certificado_autoridad_educativa "
        "FROM alumnos a "
        "JOIN escuela_bachillerato e ON e.cve_bach_ct = a.cve_bach_ct "
        "JOIN escuelas s ON s.clave_ct = e.clave_ct "
        "WHERE e.clave_ct = %s "
        "AND a.semestre = 6 "
        "AND a.alumno_estatus IN ('R', 'N', 'P') "
        "AND a.periodo_s6 = %s "
        "AND a.cve_alumno NOT IN (SELECT f.cve_alumno FROM calificaciones f WHERE f.cve_alumno=a.cve_alumno AND (f.calificacion<6 OR f.ban_acreditada='X'));"
    )
    cursor.execute(query, (fecha_cert, fecha_certificacion, nombre_autoridad, certificado_autoridad, clave, periodo))
    columnas = [col[0] for col in cursor.description]
    resultados = cursor.fetchall()
    return [dict(zip(columnas, fila)) for fila in resultados]

def insertar_registros(cursor, registros):
    for registro in registros:
        query = (
            "INSERT INTO alumno_certificado (id_hist_estudio, curp, id_proceso, certificado_digital, estatus_foto, estatus_certificado, "
                "fecha_creacion, fecha_firma, sello_sep, fecha_sello_sep, folio_sep, id_genero_ct, nombre_ct, clavecct, nivel_ct, prim_apellido, "
                "seg_apellido, nombre, promedio, fecha_cert, fecha_cert_texto, tipo_cert, entidad, cv_mun, nom_mun, observaciones_tec, "
                "sello_seduzac, fecha_certificacion, bachillerato, certificacion, autoridad_educativa, certificado_autoridad_educativa) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        )
        cursor.execute(query, (
                registro['id_hist_estudio'], registro['curp'], registro['id_proceso'], registro['certificado_digital'],
                registro['estatus_foto'], registro['estatus_certificado'], registro['fecha_creacion'], registro['fecha_firma'],
                registro['sello_sep'], registro['fecha_sello_sep'], registro['folio_sep'], registro['id_genero_ct'], 
                registro['nombre_ct'], registro['clave_ct'], registro['nivel_ct'], registro['prim_apellido'], registro['seg_apellido'],
                registro['nombre'], registro['promedio'], registro['fecha_cert'], registro['fecha_cert_texto'], registro['tipo_cert'], 
                registro['entidad'], registro['cve_mun'], registro['nom_municipio'], registro['observaciones_tec'], 
                registro['sello_seduzac'], registro['fecha_certificacion'], registro['bachillerato'],
                registro['certificacion'], registro['autoridad_educativa'], registro['certificado_autoridad_educativa']
            ))
        
def get_curp_por_escuela(cursor, clavecct):
    query = (
        "SELECT ac.curp from alumno_certificado ac "
        "JOIN alumnos a ON ac.curp = a.curp WHERE ac.clavecct = %s "
        "AND a.alumno_estatus IN ('R', 'N', 'P') "
        "AND a.cve_alumno NOT IN (SELECT f.cve_alumno FROM calificaciones f WHERE f.cve_alumno=a.cve_alumno AND (f.calificacion<6 OR f.ban_acreditada='X'));"    )
    cursor.execute(query,[clavecct])
    curp = cursor.fetchall()
    curp = curp[0]

    return curp

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
        "UPDATE alumno_certificado SET id_proceso = %s, certificado_digital = %s, estatus_certificado = %s, "
        "fecha_firma = %s, fecha_cert_texto = %s, sello_seduzac = %s WHERE curp = %s"
    )
    cursor.execute(query, [id_proceso, certificado_digital, estatus, fecha_firma, fecha_texto, sello, curp])

def datos_foliar(cursor, curp):
    query = (
        "SELECT * FROM alumno_certificado WHERE curp = %s"
    )

    cursor.execute(query,[curp])
    registros_folio = cursor.fetchone()

    # print(registros_folio)
    return registros_folio

def foliar_certificado_prepas(cursor, clavecct, curp):
    try:
        foliador_prepa = FolioLetra.objects.latest('id')
    except:
        foliador_prepa = 'A'

    clave = clavecct[2:5]
    foliador = None
    if(clave == 'EBH' or 'PBH'):
        foliador = foliador_prepa
    elif(clave == 'ETK'):
        foliador = LETRA_FOLIO_TB

    folio_sequence = FolioSequence.objects.create()
    folio_id = folio_sequence.id

    folio = f'{foliador}{str(folio_id).zfill(4)}'

    query = (
        "UPDATE alumno_certificado SET folio_sep = %s WHERE curp = %s"
    )

    cursor.execute(query,[folio,curp])

@login_required
def por_escuela(request):
    form_registros = RegistrosPorEscuelaForm(request.POST or None)
    registros_insertar = None
    error_registros_insertar = None
    mensaje_insercion = None
    boton_enviar_datos = True
    boton_firmar = False
    mensaje_firma = None
    seccion_foliador = False
    datos_foliador = None

    if(request.method == "POST"):
        with connections['mariadb'].cursor() as cursor:
            if(form_registros.is_valid()):
                clave_ct = form_registros.cleaned_data['clave_ct']
                request.session['clave_ct'] = clave_ct
                fecha_cert = form_registros.cleaned_data['fecha_certificacion']
                fecha_certificacion = form_registros.cleaned_data['fecha_certificacion']
                periodo = form_registros.cleaned_data['periodo']
                autoridad = AutoridadEducativa.objects.latest('id')
                nombre_autoridad = autoridad.nombre_autoridad
                certificado_autoridad = autoridad.certificado_autoridad
                resultados = obtener_registros_insertar(cursor, clave_ct, fecha_cert, fecha_certificacion, periodo, nombre_autoridad, certificado_autoridad)

                if('obtener_registros' in request.POST):
                    if(resultados):
                        registros_insertar = resultados
                    else:
                        error_registros_insertar = "No se encontraron registros para insertar."
                elif('insertar_datos' in request.POST):
                    if(resultados):
                        insertar_registros(cursor, resultados)
                        mensaje_insercion = "Registro insertado con éxito."
                        boton_enviar_datos = False
                        boton_firmar = True
                    else:
                        error_registros_insertar = "No se encontraron registros para insertar."
                elif('firmar' in request.POST):
                    clavecct = request.session.get('clave_ct', None)
                    if(clavecct):
                        curp = get_curp_por_escuela(cursor, clavecct)
                        valores_cadena = obtener_valores_cadena(cursor, curp)
                        firmar_certificado(cursor, curp, valores_cadena)
                        mensaje_firma = "Se firmó correctamente el certificado."
                        seccion_foliador = True
                        boton_enviar_datos = False
                        datos_foliador = datos_foliar(cursor, curp)
                elif('foliar' in request.POST):
                    clavecct = request.session.get('clave_ct', None)
                    if(clavecct):
                        curp = get_curp_por_escuela(cursor, clavecct)
                        foliar_certificado_prepas(cursor, clavecct, curp)

    return render(request,'por_esc.html',{
        'form_registros':form_registros,
        'registros_info': registros_insertar,
        'error_registros_insertar': error_registros_insertar,
        'mensaje_insertar': mensaje_insercion,
        'boton_enviar':boton_enviar_datos,
        'boton_firmar':boton_firmar,
        'mensaje_firma':mensaje_firma,
        'seccion_foliar':seccion_foliador,
        'datos_foliar':datos_foliador,
        })

# def reiniciar_foliador_pe(request):
#     mensaje = None
#     letra_form = LetraFoliadorForm(request.POST or None)
#     if(request.method == 'POST'):
#         if(letra_form.is_valid()):
#             letra_foliador = letra_form.cleaned_data['letra_foliador'].upper()
#             FolioLetraPE.objects.all().delete()
#             FolioLetraPE.objects.create(letra=letra_foliador)
#             reiniciar_secuencia_folio()
#             mensaje = f'Foliador restablecido: Letra nueva: {letra_foliador}, Secuencia restablecida a 1'

#     return render(request,"reiniciar_foliador_pe.html",{'letra_form':letra_form, 'mensaje':mensaje})

