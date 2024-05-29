from django.shortcuts import render
from .forms import CURPForm, RegistrosParcialesForm
from django.contrib.auth.decorators import login_required
from .utils import test_consulta_datos
from django.db import connection, connections


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

def obtener_clave_alumno(cursor, curp):
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

def obtener_registros_insertar(cursor, clave, fecha_cert, fecha_certificacion, bachillerato, semestre):
    query = (
        "SELECT a.cve_alumno AS id_hist_estudio, "
        "a.curp, 0 AS id_proceso, NULL AS certificado_digital, 0 AS estatus_foto, 0 AS estatus_certificado, "
        "CURDATE() AS fecha_creacion, NULL AS fecha_firma, NULL AS sello_sep ,NULL AS fecha_sello_sep, NULL AS folio_sep, "
        "s.id_genero_ct, s.nombre, e.clave_ct, NULL AS nivel_ct, TRIM(REPLACE(a.app_alumno, CHAR(9), ' ')) AS prim_apellido, "
        "TRIM(REPLACE(a.apm_alumno, CHAR(9), ' ')) AS seg_apellido, TRIM(REPLACE(a.nom_alumno, CHAR(9), ' ')) AS nombre, a.promedio, "
        "%s AS fecha_cert, NULL AS fecha_cert_texto, 4 AS tipo_cert, 32 AS entidad, '000' AS cve_mun, s.municipio AS nom_municipio, "
        "NULL AS observaciones_tec, NULL AS sello_seduzac, %s AS fecha_certificacion, %s AS bachillerato, %s AS semestre, "
        "'MARIBEL VILLALPANDO HARO. SECRETARIA DE EDUCACIÓN DEL ESTADO DE ZACATECAS.' AS autoridad_educativa, '00000000000000008682' AS certificado_autoridad_educativa "
        "FROM alumnos a "
        "JOIN escuela_bachillerato e ON e.cve_bach_ct = a.cve_bach_ct "
        "JOIN escuelas s ON s.clave_ct = e.clave_ct "
        "WHERE a.cve_alumno = %s "
        "AND a.alumno_estatus IN ('R', 'N', 'P', 'B', 'I', 'D');"
    )
    cursor.execute(query, (fecha_cert, fecha_certificacion, bachillerato, semestre, clave))
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
                registro['nombre'], registro['clave_ct'], registro['nivel_ct'], registro['prim_apellido'], registro['seg_apellido'],
                registro['nombre'], registro['promedio'], registro['fecha_cert'], registro['fecha_cert_texto'], registro['tipo_cert'], 
                registro['entidad'], registro['cve_mun'], registro['nom_municipio'], registro['observaciones_tec'], 
                registro['sello_seduzac'], registro['fecha_certificacion'], registro['bachillerato'], registro['semestre'], 
                registro['autoridad_educativa'], registro['certificado_autoridad_educativa']
            ))

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

    if(request.method == "POST"):
        with connections['mariadb'].cursor() as cursor:
            if(form_curp.is_valid()):
                curp = form_curp.cleaned_data['curp'].upper()
                alumno_info = verificar_certificado(cursor, curp)
                clave_info = obtener_clave_alumno(cursor, curp)

                if(not alumno_info):
                    error = "No se encontró el certificado"
                if(not clave_info):
                    error_clave = "No se encontró la clave del alumno"

            if(form_registros.is_valid()):
                clave = form_registros.cleaned_data['clave_alumno']
                fecha_cert = form_registros.cleaned_data['fecha_certificacion']
                fecha_certificacion = form_registros.cleaned_data['fecha_certificacion']
                bachillerato = form_registros.cleaned_data['bachillerato'].upper() or "BACHILLERATO GENERAL"
                semestre = form_registros.cleaned_data['semestre']
                resultados = obtener_registros_insertar(cursor, clave, fecha_cert, fecha_certificacion, bachillerato, semestre)

                if('obtener_registros' in request.POST):
                    if resultados:
                        registros_insertar = resultados
                    else:
                        error_registros_insertar = "No se encontraron registros para insertar."
                elif('insertar_datos' in request.POST):
                    if resultados:
                        insertar_registros(cursor, resultados)
                        mensaje_insercion = "Registro insertado con éxito."
                    else:
                        error_registros_insertar = "No se encontraron registros para insertar."

                print(f'clave: {clave}, fecha: {fecha_cert}, fecha_certificacion: {fecha_certificacion}, bachillerato: {bachillerato}')
                print(registros_insertar)

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
    })