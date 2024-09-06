from django.shortcuts import render
from django.shortcuts import render, redirect
from django.db import connection, connections
from .forms import CancelarCertForm

def buscar_certificado(cursor,curp):
    query = ("SELECT 'alumno_certificado' AS tabla, curp, prim_apellido, seg_apellido, nombre, clavecct, estatus_certificado, folio_sep, observaciones_tec "
             "FROM alumno_certificado WHERE curp = %s "
             "UNION "
             "SELECT 'alumno_cert_parcial' AS tabla, curp, prim_apellido, seg_apellido, nombre, clavecct, estatus_certificado, folio_sep, observaciones_tec "
             "FROM alumno_cert_parcial WHERE curp = %s")
    
    cursor.execute(query,[curp,curp])
    registros = cursor.fetchall()

    if(registros):
        return registros
    else:
        return None
    
def cancelar(cursor,curp, observaciones):
    registros = buscar_certificado(cursor,curp)

    if(not registros):
        return "El alumno no cuenta con un certificado."
    
    registro = registros[0]
    tabla = registro[0]

    if(tabla == 'alumno_certificado'):
        query = ("UPDATE alumno_certificado SET estatus_certificado = 3, observaciones_tec = %s WHERE curp = %s")
    elif(tabla == 'alumno_cert_parcial'):
        query = ("UPDATE alumno_cert_parcial SET estatus_certificado = 3, observaciones_tec = %s WHERE curp = %s")

    cursor.execute(query,[observaciones,curp])

    return "El certificado del alumno se canceló correctamente."

def get_estatus(cursor,curp):
    registros = buscar_certificado(cursor,curp)

    if(not registros):
        return "El alumno no cuenta con un certificado."
    
    registro = registros[0]
    tabla = registro[0]

    if(tabla == 'alumno_certificado'):
        query = ("SELECT estatus_certificado FROM alumno_certificado WHERE curp = %s")
    elif(tabla == 'alumno_cert_parcial'):
        query = ("SELECT estatus_certificado FROM alumno_cert_parcial WHERE curp = %s")

    cursor.execute(query,[curp])
    estatus = cursor.fetchone()

    if(estatus):
        return estatus[0]
    else:
        return "No se encontró estatus para el CURP proporcionado."

def cancelar_certificado(request):
    form_cancel = CancelarCertForm(request.POST or None)
    registros = None
    mensaje_registros = None
    observaciones = None
    cancelado = None
    seccion_cancelar = True
    estatus = None
    btn_cancelar = False
    mensaje_estatus = None

    if request.method == "POST":
        with connections['mariadb'].cursor() as cursor:
            if(form_cancel.is_valid()):
                if("buscar_curp" in request.POST):
                    curp = form_cancel.cleaned_data['curp'].upper()
                    registros = buscar_certificado(cursor, curp)
                    estatus = get_estatus(cursor, curp)
                    if(not registros):
                        mensaje_registros = "El alumno no cuenta con un certificado."
                    elif(registros and estatus == 3):
                        mensaje_estatus = "El certificado del alumno ya está cancelado."
                    else:
                        seccion_cancelar = True
                        btn_cancelar = True
                elif("cancelar_cert" in request.POST):
                    curp = form_cancel.cleaned_data['curp'].upper()
                    observaciones = form_cancel.cleaned_data['observaciones']
                    cancelado = cancelar(cursor, curp, observaciones)
                    seccion_cancelar = False

    return render(request, 'cancel_cert.html',{
        'form_cancel':form_cancel,
        'registros':registros,
        'mensaje_registros':mensaje_registros,
        'cancelado':cancelado,
        'seccion_cancelar':seccion_cancelar,
        'estatus':estatus,
        'btn_cancelar':btn_cancelar,
        'mensaje_estatus':mensaje_estatus,
    })
