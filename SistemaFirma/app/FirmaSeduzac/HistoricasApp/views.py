from django.shortcuts import render, redirect
from .forms import CertificacionHForm
from django.db import connection, connections
from ConfiguracionApp.models import FolioLetra, FolioSequence
from .utils import *
from FirmaSeduzac.settings import LETRA_FOLIO_TB, LETRA_FOLIO_BACHILLERATO_DISTANCIA

# fecha_cert
def get_fecha_certificado(cursor,curp):
    query = "SELECT fecha_cert FROM alumno_cert_historia WHERE curp = %s"

    cursor.execute(query,[curp])
    fecha_cert = cursor.fetchone()
    if(fecha_cert):
        fecha = fecha_cert[0]
    else:
        fecha = None

    return fecha

#fecha_certificado
def get_fecha_certificacion(cursor, curp):
    query = "SELECT fecha_certificacion FROM alumno_cert_historia WHERE curp = %s"

    cursor.execute(query,[curp])
    fecha_cert = cursor.fetchone()
    if(fecha_cert):
        fecha = fecha_cert[0]
    else:
        fecha = None

    return fecha

def buscar_certificado(cursor,curp, fecha_cert, fecha_certificacion):
    if(fecha_cert == None):
        query_fecha_cert = ("UPDATE alumno_cert_historia SET fecha_cert = %s WHERE curp = %s")
        cursor.execute(query_fecha_cert,[fecha_certificacion,curp])
    else:
        query_fecha_cert = ("UPDATE alumno_cert_historia SET fecha_certificacion = %s WHERE curp = %s")
        cursor.execute(query_fecha_cert,[fecha_cert,curp])
    query = ("SELECT id_hist_estudio, curp, estatus_certificado, folio_sep, nombre_ct, clavecct, prim_apellido, seg_apellido, nombre, "
            "promedio, fecha_cert, observaciones_tec, sello_seduzac, fecha_certificacion, bachillerato, autoridad_educativa, "
            "certificado_autoridad_educativa FROM alumno_cert_historia WHERE curp = %s")
    cursor.execute(query, [curp])
    result = cursor.fetchone()
    if(result):
        return dict(zip(['id_hist_estudio', 'curp', 'estatus_certificado', 'folio_sep', 'nombre_ct', 'clavecct', 
                         'prim_apellido', 'seg_apellido', 'nombre', 'promedio', 
                         'fecha_cert', 'observaciones_tec', 'sello_seduzac', 
                         'fecha_certificacion', 'bachillerato', 
                         'autoridad_educativa', 'certificado_autoridad_educativa'], result))
    else:
        return None
    
def obtener_estatus_certificado(cursor, curp):
    query = "SELECT estatus_certificado FROM alumno_cert_historia WHERE curp = %s"
    cursor.execute(query, [curp])

    estatus = cursor.fetchone()
    if(estatus):
        estatus_certificado = estatus[0]
    else:
        estatus_certificado = None
    return estatus_certificado


def obtener_valores_cadena(cursor, curp):
    rfc = "SAFC7105149R3"
    documento = "certificado"
    sistema = "certificacion"
    cadena = ""

    query = (
        "SELECT curp, nombre, prim_apellido, seg_apellido, promedio, clavecct FROM alumno_cert_historia "
        "WHERE curp = %s"
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
        "UPDATE alumno_cert_historia SET id_proceso = %s, certificado_digital = %s, estatus_certificado = %s, "
        "fecha_firma = %s, fecha_cert_texto = %s, sello_seduzac = %s WHERE curp = %s"
    )
    cursor.execute(query, [id_proceso, certificado_digital, estatus, fecha_firma, fecha_texto, sello, curp])

def obtener_clave_cct(cursor,curp):
    query = (
        "SELECT ac.clavecct FROM alumno_cert_historia ac WHERE ac.curp = %s"
    )
    cursor.execute(query,[curp])
    clavecct = cursor.fetchone()
    clavecct = clavecct[0]
    
    # print(f'LETRA: {LETRA_FOLIO}')
    return clavecct

def obtener_nombre_ct(cursor, curp):
    query = ("SELECT nombre_ct FROM alumno_cert_historia WHERE curp = %s;")

    cursor.execute(query,[curp])
    nombre_ct = cursor.fetchone()
    nombre_ct = nombre_ct[0]
    
    return nombre_ct

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
        "UPDATE alumno_cert_historia SET folio_sep = %s WHERE curp = %s"
    )

    cursor.execute(query,[folio,curp])

def certificaciones_historicas(request):
    form = CertificacionHForm(request.POST or None)
    alumno_info = None
    error = None
    boton_firmar = None
    seccion_datos = None
    fecha_cert = None
    fecha_certificacion = None
    mensaje_firma = None
    error_clave = None
    mensaje_firmado = None
    mensaje_no_firmado = None

    if (request.method == "POST"):
        with connections['mariadb'].cursor() as cursor:
            if(form.is_valid()):
                curp = form.cleaned_data['curp'].upper()
                request.session['curp'] = curp #Aqui guardo la curp en la sesion
                fecha_cert = get_fecha_certificado(cursor, curp)
                fecha_certificacion = get_fecha_certificacion(cursor,curp)
                alumno_info = buscar_certificado(cursor, curp, fecha_cert, fecha_certificacion)
                estatus = obtener_estatus_certificado(cursor,curp)

                if (not alumno_info):
                    error = "Este alumno no cuenta con certificado"
                    seccion_datos = True
                    boton_firmar = False
                else:
                    if(estatus in (103,1,2,4)):
                        boton_firmar = False
                        mensaje_firmado = "Este alumno ya cuenta con un certificado firmado."
                    else:
                        boton_firmar = True
                        mensaje_no_firmado = "Este alumno aún no cuenta con certificado firmado. Presione el botón de 'Firmar' si desea firmar el certificado."
                        if('firmar' in request.POST):
                            clave = obtener_clave_cct(cursor, curp)
                            if(clave == " " or clave is None or clave == ""):
                                error_clave = "El alumno no cuenta con clave de centro de trabajo. Verifique los datos."
                            else:
                                valores_cadena = obtener_valores_cadena(cursor, curp)
                                nombre_ct = obtener_nombre_ct(cursor, curp)
                                firmar_certificado(cursor, curp, valores_cadena)
                                mensaje_firma = "Se firmó correctamente el certificado."
                                boton_firmar = False
                                foliar_certificado_prepas(cursor, clave, curp, nombre_ct)
                                alumno_info = buscar_certificado(cursor, curp, fecha_cert, fecha_certificacion)
    return render(request,"cert_hist.html",{'form':form,
                                            'alumno_info':alumno_info,
                                            'error':error,
                                            'boton_firmar':boton_firmar,
                                            'seccion_datos':seccion_datos,
                                            'mensaje_firma':mensaje_firma,
                                            'error_clave':error_clave,
                                            'mensaje_firmado':mensaje_firmado,
                                            'mensaje_no_firmado':mensaje_no_firmado})