from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import connection, connections
from .forms import CertificacionPForm

def verificar_certificado(cursor, curp):
    query = "SELECT * FROM alumno_certificado WHERE curp = %s"
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
                         'fecha_certificacion', 'bachillerato', 'certificacion', 
                         'autoridad_educativa', 'certificado_autoridad_educativa'], result))
    else:
        return None
    
def obtener_clave_alumno(cursor, curp):
    query = ("SELECT * FROM alumnos WHERE curp = %s;")
    cursor.execute(query, [curp])
    clave = cursor.fetchone()
    if clave:
        return dict(zip(['cve_alumno', 'curp', 'matricula', 'generacion', 'nom_alumno', 'app_alumno', 
                         'apm_alumno', 'sexo', 'cve_bach_ct', 'periodo_s1', 'periodo_s2', 'periodo_s3', 'periodo_s4',
                          'periodo_s5', 'periodo_s6', 'promedio', 'alumno_estatus', 'folio', 'grupo', 'semestre',
                           'fecha_nac', 'direccion', 'edo_nac', 'num', 'interior', 'colonia',  'cp', 'municipio',
                            'localidad',  'estado', 'cve_form_prop', 'fecha_creacion'], clave))
    else:
        return None
    
def obtener_registros_insertar(request):
    pass

@login_required
def certificaciones_completas(request):
    alumno_info = None
    error = None
    error_clave = None
    clave_info = None
    form = CertificacionPForm(request.POST or None)

    if (request.method == "POST"):
        if(form.is_valid()):
            curp = form.cleaned_data['curp'].upper()
            with connections['mariadb'].cursor() as cursor:
                alumno_info = verificar_certificado(cursor, curp)
                clave_info = obtener_clave_alumno(cursor, curp)
            
            if not alumno_info:
                error = "No se encontró el certificado"
            if not clave_info:
                error_clave = "No se encontró la clave del alumno"

    return render(request, 'cert_compl.html', {
        'form': form,
        'alumno_info': alumno_info,
        'error': error,
        'clave': clave_info,
        'error_clave': error_clave
    })
