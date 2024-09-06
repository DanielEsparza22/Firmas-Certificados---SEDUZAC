from django.shortcuts import redirect, render
from django.db import connection, connections
from django.contrib import messages
from .utils import api_firma, fecha_a_texto, numero_a_texto
import json
from datetime import datetime
from ConfiguracionApp.models import FolioSequence, FolioLetra
from FirmaSeduzac.settings import LETRA_FOLIO_TB, LETRA_FOLIO_BACHILLERATO_DISTANCIA


def registros_sin_firma(cursor):
    query = (
        "SELECT id_hist_estudio, curp, id_proceso, estatus_certificado, clavecct, prim_apellido, seg_apellido, nombre, promedio, "
        "sello_seduzac, folio_sep, 'alumno_certificado' AS source "
        "FROM alumno_certificado WHERE estatus_certificado = 0 "
        "UNION "
        "SELECT id_hist_estudio, curp, id_proceso, estatus_certificado, clavecct, prim_apellido, seg_apellido, nombre, promedio, "
        "sello_seduzac, folio_sep, 'alumno_cert_parcial' AS source "
        "FROM alumno_cert_parcial WHERE estatus_certificado = 0;"
    )

    cursor.execute(query)
    registros = cursor.fetchall()

    # print(registros)
    return registros

def obtener_valores_cadena(cursor, curp):
    rfc = "SAFC7105149R3"
    documento = "certificado"
    sistema = "certificacion"
    cadena = ""
    tipo = ""

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




    # Antes de esta linea obtener el tipo de bachillerato
    firma = api_firma(rfc, documento, sistema, cadena, tipo)
    respuesta_json = json.loads(firma)
    sello = respuesta_json["sello"]
    uuid = respuesta_json["uuid"]
    fecha_firma = respuesta_json["fecha"]
    # print(f'SELLO : {sello}')
    # print(f'UUID : {uuid}')
    # print(f'FECHA : {fecha_firma}')

    valores_cadena = {'sello':sello, 'uuid':uuid, 'fecha':fecha_firma}

    return valores_cadena

# Obtener el nombre ct para foliar los bachilleratos a distancia
def obtener_nombre_ctp(cursor, curp):
    query = ("SELECT nombre_ct FROM alumno_cert_parcial WHERE curp = %s;")

    cursor.execute(query,[curp])
    nombre_ct = cursor.fetchone()
    nombre_ct = nombre_ct[0]
    
    return nombre_ct

def obtener_nombre_ctt(cursor, curp):
    query = ("SELECT nombre_ct FROM alumno_certificado WHERE curp = %s;")

    cursor.execute(query,[curp])
    nombre_ct = cursor.fetchone()
    nombre_ct = nombre_ct[0]
    
    return nombre_ct

def fecha_cert_texto(valores_cadena):
    fecha_texto = valores_cadena['fecha']
    fecha_res = fecha_a_texto(fecha_texto)

    return fecha_res

def firmar_certificado_cp(cursor, curp, valores_cadena):
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

def firmar_certificado_ct(cursor, curp, valores_cadena):
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

def obtener_clave_cct_cp(cursor,curp):
    query = (
        "SELECT ac.clavecct FROM alumno_cert_parcial ac WHERE ac.curp = %s"
    )
    cursor.execute(query,[curp])
    clavecct = cursor.fetchone()
    clavecct = clavecct[0]
    
    # print(f'LETRA: {LETRA_FOLIO}')
    return clavecct

def obtener_clave_cct_ct(cursor,curp):
    query = (
        "SELECT ac.clavecct FROM alumno_certificado ac WHERE ac.curp = %s"
    )
    cursor.execute(query,[curp])
    clavecct = cursor.fetchone()
    clavecct = clavecct[0]
    
    # print(f'LETRA: {LETRA_FOLIO}')
    return clavecct

def foliar_certificado_prepas_cp(cursor, clavecct, curp, nombre_ct):
    try:
        foliador_prepa = FolioLetra.objects.latest('id')
    except:
        foliador_prepa = 'A'

    clave = clavecct[2:5]
    foliador = None
    if((clave == 'EBH' or clave == 'PBH') and nombre_ct != 'BACHILLERATO A DISTANCIA'):
        foliador = foliador_prepa # --> B
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

def foliar_certificado_prepas_ct(cursor, clavecct, curp, nombre_ct):
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
        "UPDATE alumno_certificado SET folio_sep = %s WHERE curp = %s"
    )

    cursor.execute(query,[folio,curp])

def firmar(request):
    registros = None
    num_registros = 0
    with connections['mariadb'].cursor() as cursor:
        registros = registros_sin_firma(cursor)
        if(request.method == "POST"):
            registros_seleccionados = request.POST.getlist('select_registro')
            num_registros = len(registros_seleccionados)
            if(num_registros == 0):
                messages.error(request, f'Primero seleccione los registros a firmar y foliar')
            else:
                for registro_curp in registros_seleccionados:
                    # Encontrar el registro correspondiente en la lista de registros
                    registro = next((reg for reg in registros if (reg[1] == registro_curp)), None)

                    source = registro[-1] # El ultimo valor en la tupla es el source o de que tabla viene
                    if(source == 'alumno_certificado'):
                        print("Alumno Total")
                        valores_cadena = obtener_valores_cadena(cursor, registro_curp)
                        nombre_ct = obtener_nombre_ctt(cursor, registro_curp)
                        firmar_certificado_ct(cursor, registro_curp, valores_cadena)
                        clavecct = obtener_clave_cct_ct(cursor,registro_curp)
                        foliar_certificado_prepas_ct(cursor, clavecct, registro_curp, nombre_ct)

                    elif(source == 'alumno_cert_parcial'):
                        print("Alumno Parcial")
                        valores_cadena = obtener_valores_cadena(cursor, registro_curp)
                        nombre_ct = obtener_nombre_ctp(cursor, registro_curp)
                        firmar_certificado_cp(cursor, registro_curp, valores_cadena)
                        clavecct = obtener_clave_cct_cp(cursor,registro_curp)
                        foliar_certificado_prepas_cp(cursor, clavecct, registro_curp, nombre_ct)
                        
                messages.success(request, f'Se firmaron y foliaron {num_registros} certificados exitosamente')
                return redirect('firmar')

    return render(request,'firmar_foliar.html',{'registros':registros})
